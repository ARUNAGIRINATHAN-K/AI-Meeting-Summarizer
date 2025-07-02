import os

def validate_file(filename):
    allowed_extensions = ['.mp3', '.mp4', '.wav']
    return any(filename.endswith(ext) for ext in allowed_extensions)

def cleanup_files(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)