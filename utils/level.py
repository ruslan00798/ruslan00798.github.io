# utils/level.py


def calculate_level(
    xp:int
):

    level = 1

    required = 100


    remaining = xp



    while remaining >= required:

        remaining -= required

        level += 1

        required = level * 100



    return {

        "level": level,

        "current_xp": remaining,

        "need_xp": required

    }