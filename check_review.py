import asyncio
import asyncpg


async def main():

    pool = await asyncpg.create_pool(
        user="translaytor",
        password="ruslan",
        database="translaytor",
        host="localhost"
    )


    rows = await pool.fetch(
        """
        SELECT
            w.word,
            wp.correct_answers,
            wp.wrong_answers,
            wp.next_review

        FROM word_progress wp

        JOIN words w
        ON w.id = wp.word_id

        WHERE wp.telegram_id = 6599345138

        ORDER BY wp.next_review
        """
    )


    for row in rows:

        print(
            dict(row)
        )


    await pool.close()



asyncio.run(main())