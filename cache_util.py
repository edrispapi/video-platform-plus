"""Redis utilities for video caching"""
import redis
import json
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

def cache_video_metadata(video_id, metadata):
    redis_client.set(f'video_meta:{video_id}', json.dumps(metadata), ex=3600)  # کش یک‌ساعته

def get_video_metadata(video_id):
    data = redis_client.get(f'video_meta:{video_id}')
    if data:
        return json.loads(data)
    return None
