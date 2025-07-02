import os
from moviepy import VideoFileClip

def convert_video_to_audio(video_path):
    """
    Converts an mp4 video to wav audio.
    Returns the path to the audio file.
    """
    base, _ = os.path.splitext(video_path)
    audio_path = f"{base}.wav"
    
    print(f"[INFO] Converting video to audio: {video_path} → {audio_path}")
    
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # .wav format
        clip.close()
        return audio_path
    except Exception as e:
        print(f"[ERROR] Video conversion failed: {e}")
        return None
