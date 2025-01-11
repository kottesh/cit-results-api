from redis import Redis
import os

rcli = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    db=0,
    decode_responses=True
)
