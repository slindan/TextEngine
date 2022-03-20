from text import Text, Choices

t = Text
c = Choices

bath = t("It was very warm and comfy. You decide to live here.",
t("You win the game!"))

no_bath = t("As you ponder your decision, time passes and darkness ensues.",
t("You're lost forever in the darkness of the woods.",
t("You lose!")))

the_pool = t("You're at the pool. Its beaty draws you closer...",
t("Do you take a bath?",
c(["Heck yes!", "Nah, too cold!"],
[bath, no_bath])))