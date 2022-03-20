from text import Text, Choices
from pool import the_pool
t = Text
c = Choices

the_hole = t("You jump. And you fall.",
t("And fall...",
t("Aaaahhh.... so deeeep...",
t("You can't see any sign of a bottom yet.",
t("Yep. Still falling. You realize your mistake.",
t("In the near-blackness you finally make out something down there.",
t("Actually, two somethings. Which something do you aim for?",
c(["One", "Two"], [t("You're impaled on a spike. You die."), t("You landed in a pool of lava. You die.")]))))))))