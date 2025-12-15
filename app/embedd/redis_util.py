from langchain_redis import RedisConfig
import redis


redis_url = "redis://localhost:6379"

# redis_client = redis.from_url(redis_url)
#
# print(redis_client.ping())


redis_config = RedisConfig(
    redis_url=redis_url,
    index_name="langchain_redis_index",
)




