from select import select
import pygame as pg
pg.font.init()
from colors import *
from typing import List, Dict

MAX_CHARS = 90 # TODO: automatically detect this based on font and width

class Text():
    font = pg.font.SysFont('lucidaconsole', 16)
    color = GREENISH
    bg = BLACK
    padx = 3
    pady = 3
    next_text_y = pady
    anim_speed_ms = 30

    @classmethod
    def set_font(cls, new_font : pg.font):
        cls.font = new_font

    @staticmethod
    def advance_y(y):
        Text.next_text_y += y + Text.pady

    def __init__(self, text: str, next = None):
        self.text = text
        self.is_animating = False
        self.should_animate = True
        self.is_rendered = False
        self.rendered_text = ''
        self.next_anim_index = 1
        self.t = 0
        self.y = None
        self.next = next

    def get_next(self):
        return self.next

    def get_color(self):
        return type(self).color
    
    def get_bg(self):
        return type(self).bg

    def render(self, surface : pg.Surface, text_to_render = "", align : str = "left"):
        '''renders the entire text at once on the next line'''
        if not text_to_render:
            text_to_render = self.text

        text = Text.font.render(text_to_render, True, self.get_color(), self.get_bg())
        if self.y == None:
            self.y = Text.next_text_y
            Text.advance_y(text.get_rect().height)

        if align == "center":
            text_rect = text.get_rect(centerx=surface.get_width() / 2, y=self.y)
        else:
            text_rect = text.get_rect(x=Text.padx, y=self.y)

        surface.blit(text, text_rect)

        self.rendered_text = text_to_render
        if self.rendered_text == self.text:
            self.is_rendered = True
            self.should_animate = False

    def animate(self, deltaseconds, surface : pg.Surface, align : str = "left", speed_multiplier = 1.0):
        '''animates text character by character'''
        if self.is_rendered:
            return
        if not self.is_animating:
            pass
            #print (f"Animating {self.text}")
        self.is_animating = True
        self.t += deltaseconds
        if self.t >= Text.anim_speed_ms / speed_multiplier:
            self.t = 0
            text_to_render = self.text[:self.next_anim_index]
            self.next_anim_index += 1

            self.render(surface, text_to_render, align)

        if self.is_rendered:
            self.is_animating = False


class Choices(Text):
    selection = 0
    current_max_sel = 0
    active_choice = None

    @staticmethod
    def IncrementSelection():
        Choices.selection = min(Choices.selection + 1, Choices.current_max_sel)


    @staticmethod
    def DecrementSelection():
        Choices.selection = max(Choices.selection - 1, 0)

    @staticmethod
    def ConfirmActiveChoice():
        if Choices.active_choice:
           return Choices.active_choice.Confirm()

    def __init__(self, choices : List[str], outcome_texts : List[Text] = [], next : Text = None):
        super().__init__("", next)
        self.choices = choices
        self.outcome_texts = outcome_texts
        self.confirmed = False
        self.confirmed_index = 0

    def Confirm(self):
        self.confirmed = True
        self.confirmed_index = Choices.selection

        # set next
        if self.outcome_texts and self.confirmed_index < len(self.outcome_texts):
            self.next = self.outcome_texts[self.confirmed_index]

    def render(self, surface : pg.Surface, text_to_render = "", align : str = "left"):
        num = len(self.choices)
        steps = surface.get_width() / (num+1)

        for i, choice in enumerate(self.choices):
            x = steps + (steps * i)
            text = Text.font.render(choice, True, self.get_color(i), self.get_bg(i))
            if self.y == None:
                self.y = Text.next_text_y
                Text.advance_y(text.get_rect().height)

            text_rect = text.get_rect(centerx=x, y=self.y)
            surface.blit(text, text_rect)

        if not self.is_rendered:
            Choices.active_choice = self
            Choices.current_max_sel = len(self.choices) - 1
            Choices.selection = 0
        self.is_rendered = True

    def animate(self, deltaseconds, surface: pg.Surface, align: str = "left", speed_multiplier=1):
        self.render(surface)

        if not self.confirmed:
            self.is_animating = True
            self.should_animate = True
        else:
            self.is_animating = False
            self.should_animate = False

    def get_color(self, i):
        if self.confirmed and self.confirmed_index == i:
            return BLACK
        return RED if Choices.selection == i else YELLOW

    def get_bg(self, i):
        if self.confirmed and self.confirmed_index == i:
            return GREENISH
        return WHITE if Choices.selection == i else super().get_bg()

class TextList(list):
    pause_time_ms = 300
    def __init__(self, *args, parse_text = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.is_pausing = False
        self.t = 0

        if parse_text:
            # parse a str into lines of Text
            if isinstance(parse_text, list):
                parse_text = "\n".join(parse_text)
            lines = parse_text.split("\n")
            for line in lines:
                self.append(Text(line))


    def animate(self, deltaseconds, surface : pg.Surface, align : str = "left", speed_multiplier = 1.0):
        if self.is_pausing:
            self.t += deltaseconds
            if self.t >= TextList.pause_time_ms:
                self.t = 0
                self.is_pausing = False
            else:
                return 

        texts_to_animate = [x for x in self if isinstance(x, Text) and x.should_animate]
        if texts_to_animate:
            texts_to_animate[0].animate(deltaseconds, surface, align, speed_multiplier)
            if not texts_to_animate[0].is_animating:
                next = texts_to_animate[0].get_next()
                if next:
                    self.append(next)
                self.pop(0)
                self.is_pausing = True
            