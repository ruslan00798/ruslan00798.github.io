import asyncio

from database.redis_client import redis


async def main():
    print("PING:", await redis.ping())

    keys = await redis.keys("*")

    print("\nREDIS KEYS:")

    if not keys:
        print("Redis пока пустой")
    else:
        for key in keys:
            print(key)

    await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
