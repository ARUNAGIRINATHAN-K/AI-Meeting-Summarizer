import subprocess
import os

WHISPER_PATH = "C:\Users\aruna\OneDrive\Desktop\ai_meeting_summarizer\whisper_bin\main.exe"  # or "whisper_bin/main.exe" on Windows
MODEL_PATH = "C:\Users\aruna\OneDrive\Desktop\ai_meeting_summarizer\whisper.cpp\models"

def transcribe_audio(audio_path):
    """
    Runs Whisper.cpp on an audio file and returns the transcript text.
    """
    output_dir = "transcripts"
    os.makedirs(output_dir, exist_ok=True)

    command = [
        WHISPER_PATH,
        "-m", MODEL_PATH,
        "-f", audio_path,
        "-otxt",            # Output .txt format
        "-of", os.path.join(output_dir, "transcript")
    ]

    print(f"[INFO] Transcribing with Whisper.cpp: {audio_path}")
    try:
        subprocess.run(command, check=True)
        transcript_file = os.path.join(output_dir, "transcript.txt")
        with open(transcript_file, "r", encoding="utf-8") as f:
            return f.read()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Transcription failed: {e}")
        return ""
