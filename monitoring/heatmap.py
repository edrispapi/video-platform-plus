import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def track_watch_time(video_id, second):
    """
    ثبت بازدید ثانیه به ثانیه (برای تولید heatmap)
    """
    redis_client.hincrby(f"video:{video_id}:heatmap", second, 1)

def get_heatmap(video_id):
    """
    بازگرداندن نمودار هیت‌مپ هر ویدیو برای تحلیل
    """
    data = redis_client.hgetall(f"video:{video_id}:heatmap")
    return {int(k): int(v) for k, v in data.items()}
