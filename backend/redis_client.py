import redis
import os

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Redis Client Instance
redis_client = redis.StrictRedis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=REDIS_DB, 
    decode_responses=True
)

# Optional: Test connection function
def test_redis_connection():
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
        return True
    except redis.ConnectionError:
        print("❌ Redis connection failed!")
        return False