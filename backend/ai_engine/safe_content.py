def classify_unsafe_content(frame, nsfw_model):
    """تشخیص محتوای نامناسب با مدل NSFW"""
    preds = nsfw_model.predict(frame)
    return preds.get('unsafe', 0) > 0.5
