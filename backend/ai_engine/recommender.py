from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_user_feature_vector(user_id, user_video_logs, video_embeddings):
    """
    ساخت بردار کاربر بر اساس سابقه تماشای ویدیوها و embeddingهای هر ویدیو
    """
    watched_video_ids = user_video_logs[user_id]
    features = [video_embeddings[vid] for vid in watched_video_ids if vid in video_embeddings]
    if not features:
        return np.zeros_like(next(iter(video_embeddings.values())))
    return np.mean(features, axis=0)

def recommend_videos(user_id, user_video_logs, video_embeddings, top_k=10):
    """
    پیشنهاد ویدیو به کاربر بر اساس شباهت ویژگی‌ها (خودکفای مبتنی بر content embedding)
    """
    user_vec = get_user_feature_vector(user_id, user_video_logs, video_embeddings)
    all_video_ids = list(video_embeddings.keys())
    video_vecs = np.stack([video_embeddings[vid] for vid in all_video_ids])
    scores = cosine_similarity([user_vec], video_vecs)[0]
    rec_indices = scores.argsort()[-top_k:][::-1]
    return [all_video_ids[i] for i in rec_indices]
