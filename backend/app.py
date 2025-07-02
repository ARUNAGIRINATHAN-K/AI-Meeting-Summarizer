from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from transcriber import transcribe_audio
from summarizer import summarize_text, extract_action_items
from utils import convert_video_to_audio

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'm4a'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print("[INFO] File saved:", filepath)

        # Convert to audio if needed
        if filename.endswith('.mp4'):
            audio_path = convert_video_to_audio(filepath)
        else:
            audio_path = filepath

        # Transcribe
        transcript = transcribe_audio(audio_path)

        # Summarize
        summary = summarize_text(transcript)

        # Extract action items
        actions = extract_action_items(transcript)

        return jsonify({
            'summary': summary,
            'action_items': actions
        })

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(debug=True)
