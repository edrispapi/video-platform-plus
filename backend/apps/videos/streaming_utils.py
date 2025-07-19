import subprocess

def generate_hls(input_path, output_m3u8):
    """تولید استریم HLS"""
    subprocess.run(["ffmpeg", "-i", input_path, "-codec:", "copy", "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0", "-f", "hls", output_m3u8], check=True)

def generate_dash(input_path, output_mpd):
    """تولید استریم DASH"""
    subprocess.run(["ffmpeg", "-i", input_path, "-map", "0", "-f", "dash", output_mpd], check=True)
