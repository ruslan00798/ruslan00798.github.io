import asyncio
import aiohttp
import asyncpg
import ssl
import certifi


API_KEY = "56751720-06845450ed3968c7e3138b6d1"


async def main():

    pool = await asyncpg.create_pool(
        user="translaytor",
        password="ruslan",
        database="translaytor",
        host="localhost"
    )


    words = await pool.fetch(
        """
        SELECT
            id,
            word

        FROM words

        WHERE image_url IS NULL
        """
    )


    print(
        "Слов без картинок:",
        len(words)
    )


    ssl_context = ssl.create_default_context(
        cafile=certifi.where()
    )


    connector = aiohttp.TCPConnector(
        ssl=ssl_context
    )


    async with aiohttp.ClientSession(
        connector=connector
    ) as session:


        for item in words:

            word = item["word"]


            if len(word) <= 2:

                print(
                    "⏭ Пропуск:",
                    word
                )

                continue


            params = {
                "key": API_KEY,
                "q": word,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": 3
            }


            try:

                async with session.get(
                    "https://pixabay.com/api/",
                    params=params
                ) as response:


                    data = await response.json()


                    hits = data.get("hits")


                    if hits:


                        # сохраняем прямую ссылку CDN
                        image = hits[0]["previewURL"]


                        await pool.execute(
                            """
                            UPDATE words

                            SET image_url=$1

                            WHERE id=$2
                            """,
                            image,
                            item["id"]
                        )


                        print(
                            "✅",
                            word
                        )


                    else:

                        print(
                            "❌ Нет картинки:",
                            word
                        )


            except Exception as error:

                print(
                    "ERROR:",
                    word,
                    error
                )


            await asyncio.sleep(0.5)


    await pool.close()



asyncio.run(main())