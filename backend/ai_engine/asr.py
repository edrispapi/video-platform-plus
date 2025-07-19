import subprocess

def audio_to_text(audio_path, output_txt):
    """
    تبدیل صوت ویدیو به متن با استفاده از مدل pre-trained مانند Whisper.
    """
    subprocess.run([
        "whisper", audio_path, "--language", "fa", "--output", output_txt
    ], check=True)  # اضافه کردن check=True برای مدیریت خطاها
    with open(output_txt, "r", encoding="utf-8") as f:
        caption = f.read()
    return caption

def extract_audio_for_transcription(video_path):
    import os
    audio_out = video_path.replace('.mp4', '_sub.wav')
    subprocess.run(['ffmpeg', '-i', video_path, '-vn', audio_out], check=True)
    return audio_out
