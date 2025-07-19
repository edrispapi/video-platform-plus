import subprocess

def whisper_transcribe(audio_path, lang="fa"):
    """تبدیل صوت به متن با OpenAI Whisper"""
    output_txt = audio_path.replace(".wav", ".txt")
    subprocess.run(["whisper", audio_path, "--language", lang, "--output", output_txt], check=True)
    with open(output_txt, "r", encoding="utf-8") as f:
        text = f.read()
    return text
