from channels.layers import get_channel_layer
import asyncio

async def send_live_poll(video_room, poll_data):
    """ارسال نظرسنجی زنده به کاربران"""
    channel_layer = get_channel_layer()
    await channel_layer.group_send(video_room, {"type": "live.poll", "poll": poll_data})

def create_poll(video_id, question, options):
    """ایجاد نظرسنجی برای ویدئو"""
    return {
        "video_id": video_id,
        "question": question,
        "options": options,
        "votes": {opt: 0 for opt in options}
    }
