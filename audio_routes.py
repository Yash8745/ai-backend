from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

audio_routes = Blueprint('audio_routes', __name__)

# Define the uploads directory using an absolute path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}

# Attempt to create the uploads directory if it doesn't exist
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"Uploads folder created or already exists at: {UPLOAD_FOLDER}")
except OSError as e:
    print(f"Error creating uploads folder: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_routes.route('/audio/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)

        try:
            # Debugging: Log file details
            audio.seek(0)  # Reset file pointer before checking size
            print(f"Received file: {filename}, Type: {audio.mimetype}")
            print(f"Size: {len(audio.read())} bytes")
            audio.seek(0)  # Reset file pointer again after reading

            # Check if the MIME type is audio/*
            if not audio.mimetype.startswith('audio/'):
                return jsonify({'error': 'Invalid file type. Must be an audio file'}), 400

            # Save the file
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            audio.save(file_path)

            # Debugging: Log successful file save
            print(f"Audio file saved at {file_path}")

            # Mock processing response
            response = {
                'message': 'Audio processed and vector stored successfully',
                'filename': filename
            }

            return jsonify(response)

        except Exception as e:
            print(f"Error processing audio file: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only .wav, .mp3, .ogg, .flac, .m4a files are allowed'}), 400
