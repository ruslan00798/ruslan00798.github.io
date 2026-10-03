import logging

import asyncpg

from config import settings

from datetime import date, timedelta

logger = logging.getLogger(__name__)


pool = None


async def connect_db():

    global pool

    pool = await asyncpg.create_pool(
        user=settings.db_user,
        password=settings.db_pass,
        database=settings.db_name,
        host=settings.db_host,
        port=settings.db_port,
    )

    logger.info("Database connection pool created")

async def close_db():
    global pool

    if pool is not None:
        await pool.close()
        pool = None

        logger.info("Database connection pool closed")



# ==========================
# Пользователь / язык
# ==========================

async def update_language(
    user_id: int,
    language: str
):


    await pool.execute(

        """
        INSERT INTO users(
            telegram_id,
            language,
            xp
        )

        VALUES(
            $1,
            $2,
            0
        )


        ON CONFLICT(telegram_id)

        DO UPDATE SET

            language = EXCLUDED.language

        """,

        user_id,
        language

    )





async def get_language(
    user_id: int
):


    return await pool.fetchval(

        """
        SELECT language

        FROM users

        WHERE telegram_id = $1

        """,

        user_id

    )





# ==========================
# История переводов
# ==========================

async def save_history(

    user_id: int,

    text: str,

    translated: str

):


    await pool.execute(

        """
        INSERT INTO users(
            telegram_id
        )

        VALUES($1)

        ON CONFLICT DO NOTHING

        """,

        user_id

    )



    row = await pool.fetchrow(

        """
        INSERT INTO history(

            telegram_id,

            original_text,

            translated_text,

            next_review,

            review_interval

        )

        VALUES(

            $1,

            $2,

            $3,

            NOW(),

            1

        )


        RETURNING id

        """,

        user_id,

        text,

        translated

    )


    return row["id"]





async def get_history(

    user_id: int,

    limit: int = 10,

    offset: int = 0

):


    return await pool.fetch(

        """
        SELECT

            id,

            original_text,

            translated_text,

            created_at


        FROM history


        WHERE telegram_id = $1


        ORDER BY created_at DESC


        LIMIT $2

        OFFSET $3

        """,

        user_id,

        limit,

        offset

    )





async def get_history_by_id(

    user_id: int,

    history_id: int

):


    return await pool.fetchrow(

        """
        SELECT

            id,

            original_text,

            translated_text


        FROM history


        WHERE id = $1

        AND telegram_id = $2

        """,

        history_id,

        user_id

    )





async def clear_history(

    user_id: int

):


    await pool.execute(

        """
        DELETE FROM history

        WHERE telegram_id = $1

        """,

        user_id

    )





async def delete_history(

    user_id: int,

    history_id: int

) -> bool:
   


    result = await pool.execute(

        """
        DELETE FROM history

        WHERE id = $1

        AND telegram_id = $2

        """,

        history_id,

        user_id

    )

    return result == "DELETE 1"


# ==========================
# XP
# ==========================

async def add_xp(user_id: int, xp: int):
    if xp <= 0:
        return

    await pool.execute(
        """
        INSERT INTO users(
            telegram_id,
            xp
        )
        VALUES(
            $1,
            $2
        )
        ON CONFLICT(telegram_id)
        DO UPDATE SET
            xp = users.xp + EXCLUDED.xp
        """,
        user_id,
        xp
    )





async def get_xp(user_id: int) -> int:
    xp = await pool.fetchval(

        """
        SELECT xp

        FROM users

        WHERE telegram_id = $1

        """,
        user_id
    )
    return xp or 0


# ==========================
# Избранное
# ==========================

async def toggle_favorite(

    user_id: int,

    history_id: int

):


    return await pool.fetchval(

        """
        UPDATE history

        SET favorite = NOT favorite


        WHERE id = $1

        AND telegram_id = $2


        RETURNING favorite

        """,

        history_id,

        user_id

    )

# ==========================
# Удалить из избранного
# ==========================
async def remove_favorite(

    user_id: int,

    history_id: int

):

    return await pool.fetchval(

        """
        UPDATE history

        SET favorite = FALSE

        WHERE id = $1

        AND telegram_id = $2

        RETURNING favorite

        """,

        history_id,

        user_id

    )


async def get_favorites(

    user_id: int

):


    return await pool.fetch(

        """
        SELECT

            id,

            original_text,

            translated_text

           


        FROM history


        WHERE telegram_id = $1

        AND favorite = TRUE


        ORDER BY created_at DESC

        """,

        user_id

    )





async def get_statistics(

    user_id: int

):


    row = await pool.fetchrow(

        """
        SELECT

            COUNT(*) AS translations,


            COUNT(*) FILTER(

                WHERE favorite = TRUE

            ) AS favorites


        FROM history


        WHERE telegram_id = $1

        """,

        user_id

    )


    return {

        "translations": row["translations"] or 0,

        "favorites": row["favorites"] or 0

    }





# ==========================
# Обучение переводов
# ==========================




async def get_study_progress(

    user_id: int

):


    return await pool.fetchrow(

        """
        SELECT


            COUNT(*) AS total_words,


            COUNT(*) FILTER(

                WHERE study_known > 0

            ) AS learned_words,


            COUNT(*) FILTER(

                WHERE study_unknown > 0

            ) AS difficult_words


        FROM history


        WHERE telegram_id = $1

        """,

        user_id

    )





async def get_learned_words(

    user_id: int

):


    count = await pool.fetchval(

        """
        SELECT COUNT(*)

        FROM history


        WHERE telegram_id = $1


        AND study_known > 0

        """,

        user_id

    )


    return count or 0

# ==========================
# Серия дней
# ==========================

async def update_streak(
    user_id: int
):

    today = date.today()



    row = await pool.fetchrow(

        """
        SELECT

            streak,

            last_activity


        FROM users


        WHERE telegram_id = $1

        """,

        user_id

    )



    if not row:


        await pool.execute(

            """
            INSERT INTO users(

                telegram_id,

                streak,

                last_activity

            )


            VALUES(

                $1,

                1,

                $2

            )

            """,

            user_id,

            today

        )


        return 1, True




    streak = row["streak"] or 0

    last = row["last_activity"]




    if last == today:


        return streak, False




    if last == today - timedelta(days=1):


        streak += 1


    else:


        streak = 1





    await pool.execute(

        """
        UPDATE users


        SET

            streak = $1,

            last_activity = $2


        WHERE telegram_id = $3

        """,

        streak,

        today,

        user_id

    )



    return streak, True





# ==========================
# Дневная цель
# ==========================

async def update_daily_goal(

    user_id: int

):


    today = date.today()



    await pool.execute(

        """
        INSERT INTO daily_goal(

            telegram_id,

            goal_date,

            completed,

            target

        )


        VALUES(

            $1,

            $2,

            0,

            10

        )


        ON CONFLICT(telegram_id)


        DO UPDATE SET


            goal_date =

                CASE

                    WHEN daily_goal.goal_date <> EXCLUDED.goal_date

                    THEN EXCLUDED.goal_date

                    ELSE daily_goal.goal_date

                END,


            completed =

                CASE

                    WHEN daily_goal.goal_date <> EXCLUDED.goal_date

                    THEN 0

                    ELSE daily_goal.completed

                END

        """,

        user_id,

        today

    )





async def add_daily_progress(

    user_id: int

):


    await pool.execute(

        """
        UPDATE daily_goal


        SET completed = completed + 1


        WHERE telegram_id = $1

        """,

        user_id

    )





async def get_daily_goal(

    user_id: int

):


    row = await pool.fetchrow(

        """
        SELECT

            completed,

            target


        FROM daily_goal


        WHERE telegram_id = $1

        """,

        user_id

    )



    if not row:


        return {

            "completed": 0,

            "target": 10

        }



    return row





# ==========================
# Новые слова
# ==========================

async def get_random_word(
    user_id: int,
    language: str,
    category: str = "all",
    level: str = "A1",
):
    return await pool.fetchrow(
    """
    SELECT
        w.id,
        w.word,
        w.translation,
        w.image_url,
        w.language,
        w.category,
        w.level
    FROM words w

    LEFT JOIN word_progress wp
        ON wp.word_id = w.id
        AND wp.telegram_id = $1

    WHERE w.language = $2

    AND (
        $3 = 'all'
        OR w.category = $3
    )

    AND w.level = $4

    AND
(
    wp.word_id IS NULL

    OR

    wp.learned = FALSE

    OR

    wp.next_review <= NOW()
)

    ORDER BY RANDOM()

    LIMIT 1
    """,
    user_id,
    language,
    category,
    level
)



async def save_word_answer(
    user_id: int,
    word_id: int,
    correct: bool
):

    """
    Сохраняет результат ответа пользователя
    и рассчитывает следующую дату повторения.
    """

    if correct:

        await pool.execute(
            """
            INSERT INTO word_progress
            (
                telegram_id,
                word_id,
                learned,
                correct_answers,
                wrong_answers,
                next_review,
                learning_stage
            )

            VALUES
            (
                $1,
                $2,
                FALSE,
                1,
                0,
                NOW() + INTERVAL '3 days',
                1
            )

            ON CONFLICT
            (
                telegram_id,
                word_id
            )

            DO UPDATE SET

                correct_answers =
                    word_progress.correct_answers + 1,

                learned =
                    CASE
                        WHEN word_progress.correct_answers >= 3
                            THEN TRUE
                        ELSE FALSE
                    END,
                
                next_review =
                    CASE
                        WHEN word_progress.correct_answers = 0
                            THEN NOW() + INTERVAL '3 days'

                        WHEN word_progress.correct_answers = 1
                            THEN NOW() + INTERVAL '7 days'

                        WHEN word_progress.correct_answers = 2
                            THEN NOW() + INTERVAL '14 days'

                        ELSE NOW() + INTERVAL '30 days'
                    END,

                learning_stage =
                    CASE
                        WHEN word_progress.correct_answers = 0
                            THEN 1

                        WHEN word_progress.correct_answers = 1
                            THEN 2

                        WHEN word_progress.correct_answers = 2
                            THEN 3

                        ELSE 4
                    END
            """,

            user_id,
            word_id
        )

    else:

        await pool.execute(
            """
            INSERT INTO word_progress
            (
                telegram_id,
                word_id,
                learned,
                correct_answers,
                wrong_answers,
                next_review,
                learning_stage
            )

            VALUES
            (
                $1,
                $2,
                FALSE,
                0,
                1,
                NOW() + INTERVAL '1 day',
                0
            )

            ON CONFLICT
            (
                telegram_id,
                word_id
            )

            DO UPDATE SET

                learned = FALSE,

                wrong_answers =
                    word_progress.wrong_answers + 1,

                next_review =
                    NOW() + INTERVAL '1 day',

                learning_stage = 0
            """,

            user_id,
            word_id
        )

    logger.info(
        "Word answer saved: user_id=%s word_id=%s correct=%s",
        user_id,
        word_id,
        correct,
    )        


async def get_word_for_review(

    user_id: int,

    language: str

):


    return await pool.fetchrow(

        """
        SELECT


            w.id,

            w.word,

            w.translation,

            w.image_url


        FROM word_progress wp


        JOIN words w

            ON w.id = wp.word_id



        WHERE wp.telegram_id = $1


        AND w.language = $2


        AND wp.next_review <= NOW()



        ORDER BY wp.next_review



        LIMIT 1

        """,

        user_id,

        language

    )

# ==========================
# Количество слов на повторение
# ==========================

async def get_review_count(
    user_id: int
):

    count = await pool.fetchval(

        """
        SELECT COUNT(*)

        FROM word_progress wp

        WHERE wp.telegram_id = $1

        AND wp.next_review <= NOW()

        """,

        user_id

    )


    return count or 0

async def get_word(word: str, language: str):

    

    result = await pool.fetchrow(
        """
        SELECT *
        FROM words
        WHERE LOWER(word)=LOWER($1)
          AND language = $2
        LIMIT 1
        """,
        word,
        language
    )

    

    return result


async def create_word(
    word: str,
    translation: str,
    language: str = "en",
    category: str = "general",
    level: str = "1",
):

    row = await pool.fetchrow(
        """
        INSERT INTO words
        (
            word,
            translation,
            language,
            category,
            level
        )

        VALUES
        (
            $1,
            $2,
            $3,
            $4,
            $5
        )

        RETURNING id
        """,
        word,
        translation,
        language,
        category,
        level
    )

    return row["id"]


async def get_random_translations(exclude_word_id: int, limit: int = 3):

    return await pool.fetch(
        """
        SELECT id, translation
        FROM words
        WHERE id <> $1
        ORDER BY RANDOM()
        LIMIT $2
        """,
        exclude_word_id,
        limit
    )    

async def add_word_progress(
    user_id: int,
    word_id: int
):

    await pool.execute(
        """
        INSERT INTO word_progress
        (
            telegram_id,
            word_id,
            learned,
            correct_answers,
            wrong_answers,
            next_review,
            streak,
            learning_stage
        )

        VALUES
        (
            $1,
            $2,
            FALSE,
            0,
            0,
            NOW(),
            0,
            1
        )

        ON CONFLICT DO NOTHING
        """,

        user_id,
        word_id
    )

async def get_wrong_answers(
    word_id: int
):

    return await pool.fetch(
        """
        SELECT translation

        FROM words

        WHERE id != $1

        ORDER BY RANDOM()

        LIMIT 3
        """,

        word_id
    )    

async def get_word_by_id(
    word_id: int
):

    return await pool.fetchrow(
        """
        SELECT
            id,
            word,
            translation,
            language,
            category,
            image_url

        FROM words

        WHERE id = $1
        """,
        word_id
    )


async def update_session_result(
    user_id: int,
    correct: bool
):
    try:

        await pool.execute(
            """
            INSERT INTO study_session(
                telegram_id,
                total_answers,
                correct_answers,
                wrong_answers
            )

            VALUES(
                $1,
                1,
                $2,
                $3
            )

            ON CONFLICT(telegram_id)

            DO UPDATE SET

                total_answers =
                    study_session.total_answers + 1,

                correct_answers =
                    study_session.correct_answers + $2,

                wrong_answers =
                    study_session.wrong_answers + $3

            """,

            user_id,

            1 if correct else 0,

            0 if correct else 1
        )

        logger.info(
            "Study session updated: user_id=%s correct=%s",
            user_id,
            correct
        )
        
    except Exception:
        logger.exception(
            "Failed to update study session: user_id=%s correct=%s",
            user_id,
            correct
        )
        raise
            

async def get_session_result(
    user_id: int
):

    row = await pool.fetchrow(
        """
        SELECT

            total_answers,
            correct_answers,
            wrong_answers

        FROM study_session

        WHERE telegram_id = $1

        """,

        user_id
    )


    if not row:

        return {
            "total_answers": 0,
            "correct_answers": 0,
            "wrong_answers": 0
        }


    return row

async def finish_session(
    user_id: int
):

    row = await pool.fetchrow(
        """
        SELECT

            total_answers,
            correct_answers,
            wrong_answers

        FROM study_session

        WHERE telegram_id = $1

        """,

        user_id
    )


    await pool.execute(
        """
        DELETE FROM study_session

        WHERE telegram_id = $1
        """,

        user_id
    )


    return row     



async def save_learning_session(
    telegram_id: int,
    category: str,
    level: str,
    mode: str = "new"
):

    await pool.execute(
        """
                    INSERT INTO learning_session
            (
            telegram_id,
            category,
            level,
            mode
            )

            VALUES
            (
            $1,
            $2,
            $3,
            $4
            )

            ON CONFLICT (telegram_id)

            DO UPDATE SET

            category = EXCLUDED.category,
            level = EXCLUDED.level,
            mode = EXCLUDED.mode,
            updated_at = NOW()
        """,
        telegram_id,
        category,
        level,
        mode
    ) 

async def get_learning_session(
    telegram_id: int
):

    return await pool.fetchrow(
        """
        SELECT
            category,
            level

        FROM learning_session

        WHERE telegram_id = $1
        """,
        telegram_id
    )

async def get_random_wrong_word(
    telegram_id: int,
    language: str
):

    return await pool.fetchrow(
        """
        SELECT
            w.id,
            w.word,
            w.translation,
            w.image_url,
            w.language,
            w.category,
            w.level

        FROM words w

        JOIN word_progress wp
            ON wp.word_id = w.id

        WHERE
            wp.telegram_id = $1

            AND wp.wrong_answers > 0

           

            AND (
                wp.learned = FALSE
                OR wp.wrong_answers >= wp.correct_answers
            )

            AND w.language = $2


        ORDER BY
            wp.wrong_answers DESC,
            RANDOM()


        LIMIT 1
        """,

        telegram_id,
        language
    )


async def get_new_word(
    telegram_id,
    language,
    category,
    level
):

    return await pool.fetchrow(
    """
    SELECT
        w.*

    FROM words w


    LEFT JOIN word_progress wp

    ON wp.word_id = w.id

    AND wp.telegram_id = $1


    WHERE

    w.language = $2

    AND w.level = $4


    AND
    (
        $3='all'
        OR w.category=$3
    )


    AND wp.word_id IS NULL


    ORDER BY RANDOM()

    LIMIT 1

    """,

    telegram_id,
    language,
    category,
    level
    )


async def get_review_word(
    telegram_id: int,
    language: str
):

    result = await pool.fetchrow(
        """
        SELECT
            w.id,
            w.word,
            w.translation,
            w.image_url,
            w.language,
            w.category,
            w.level
        FROM words w
        JOIN word_progress wp
            ON wp.word_id = w.id
        WHERE
            wp.telegram_id = $1
            AND w.language = $2
            AND wp.next_review <= NOW()
            AND wp.learned = FALSE
        ORDER BY RANDOM()
        LIMIT 1
        """,
        telegram_id,
        language
    )

    print("GET REVIEW WORD:", result)

    return result

async def get_random_picture_word():

    word = await pool.fetchrow(
        """
        SELECT
            id,
            word,
            translation,
            image_url

        FROM words

        WHERE image_url IS NOT NULL

        ORDER BY RANDOM()

        LIMIT 1
        """
    )

    return word

