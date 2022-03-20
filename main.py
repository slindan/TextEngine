import pygame as pg
from colors import *
from text import Choices, Text, TextList

WIDTH, HEIGHT = 910, 900

def main():
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.SCALED)
    pg.display.set_caption("Game jam!")
    #pg.mouse.set_visible(False)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    from story import story
    l = TextList()
    l.append(story)

    # clock object limits FPS
    clock = pg.time.Clock()
    game_on = True
    while game_on:
        clock.tick(60)
        screen.blit(background, (0, 0))
        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game_on = False
                elif event.key == pg.K_LEFT:
                    Choices.DecrementSelection()
                elif event.key == pg.K_RIGHT:
                    Choices.IncrementSelection()
                elif event.key == pg.K_RETURN:
                    Choices.ConfirmActiveChoice()

        l.animate(clock.get_time(), background, "center", 1.2)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()