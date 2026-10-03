
import asyncio
from redis.asyncio import Redis

async def main():
    redis = Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    try:
        result = await redis.ping()
        print("REDIS:", result)
    except Exception as e:
        print("ERROR:", type(e).__name__, e)
    finally:
        await redis.aclose()

asyncio.run(main())
