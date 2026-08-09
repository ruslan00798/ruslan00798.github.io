import asyncio
import asyncpg


async def main():

    conn = await asyncpg.connect(
        user="translaytor",
        password="ruslan",
        database="translaytor",
        host="localhost"
    )


    word = await conn.fetchrow(
        """
        SELECT
            w.word,
            wp.wrong_answers,
            wp.learned

        FROM words w

        JOIN word_progress wp
            ON wp.word_id = w.id

        WHERE
            wp.telegram_id = 6599345138
            AND wp.wrong_answers > 0

        LIMIT 10
        """
    )


    print(word)


    await conn.close()


asyncio.run(main())