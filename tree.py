from text import Text, Choices
from pool import the_pool
t = Text
c = Choices

from pool import the_pool

screw_it = t("You let go.", t("You fall for ages, but the ground is so soft from all the moss,",
t("it dampens your fall and you survive.",
t("You look around...", the_pool))))

press_on = t("You strain and make the weirdest noises as you climb.",
t("Eventually, exhausted, you find a giant birds nest. You curl up and fall asleep.",
t("After an hour of blissful sleep, you get eaten by a giant bird.",
t("You lose!"))))

the_tree = t("You start climbing. You climb and climb",
t("...and climb.",
t("It never seems to end!",
t("Your arms get tired. You can barely hold on! Do you give up, or press on?",
c(["Yeah, screw this!", "Press on!"],
[screw_it, press_on])))))