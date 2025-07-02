from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from whisper import transcribe_audio
from summarizer import summarize_text, extract_action_items
from utils import validate_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if not validate_file(file.filename):
        return jsonify({'error': 'Invalid file format'}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # Transcribe
        transcription = transcribe_audio(file_path)
        transcription_path = os.path.join(OUTPUT_FOLDER, f"{filename}.txt")
        with open(transcription_path, 'w') as f:
            f.write(transcription)

        # Summarize and extract action items
        summary = summarize_text(transcription)
        action_items = extract_action_items(transcription)

        return jsonify({
            'transcription': transcription,
            'summary': summary,
            'action_items': action_items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)