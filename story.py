from text import Text, Choices
from pool import the_pool
from tree import the_tree
from hole import the_hole
t = Text
c = Choices

story = t("You find yourself deep in a murky wood.", 
t("In front of you there is a shimmering pool of water.",
t("To your right you see a giant, ancient oak tree.",
t("To your left there is a deep hole... You wonder how deep it goes.",
t("What do you do?",
c(["Go to the pool", "Climb the tree",  "Jump down the hole"],
[the_pool, the_tree, the_hole]))))))