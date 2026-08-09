# utils/achievements.py


ACHIEVEMENTS = [

    {
        "name": "Первый перевод",
        "condition": lambda translations, xp, learned:
            translations >= 1
    },

    {
        "name": "10 переводов",
        "condition": lambda translations, xp, learned:
            translations >= 10
    },

    {
        "name": "100 переводов",
        "condition": lambda translations, xp, learned:
            translations >= 100
    },

    {
        "name": "Получено 100 XP",
        "condition": lambda translations, xp, learned:
            xp >= 100
    },

    {
        "name": "50 изученных слов",
        "condition": lambda translations, xp, learned:
            learned >= 50
    },

]


def get_achievements(
    translations: int,
    xp: int,
    learned: int
):

    result = []


    for achievement in ACHIEVEMENTS:


        if achievement["condition"](
            translations,
            xp,
            learned
        ):

            result.append(
                "✅ " + achievement["name"]
            )

        else:

            result.append(
                "🔒 " + achievement["name"]
            )


    return result