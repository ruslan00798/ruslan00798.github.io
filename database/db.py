import asyncpg

pool = None


async def connect_db():

    global pool

    pool = await asyncpg.create_pool(
        user="translaytor",
        password="ruslan",
        database="translaytor",
        host="localhost",
        port=5432
    )

    db = await pool.fetchval(
        "SELECT current_database()"
    )

    print("CONNECTED DB:", db)