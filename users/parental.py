def check_video_for_kid(profile, video_tags):
    """کنترل محتوای مناسب برای کودکان"""
    allowed_tags = profile.preferences.get("allowed_tags", ["cartoon", "edu"])
    return all(tag in allowed_tags for tag in video_tags)
