from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

audio_routes = Blueprint('audio_routes', __name__)

UPLOAD_FOLDER = 'uploads'  # Directory where audio files will be saved
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}  # Allowed audio file types

# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload audio route
@audio_routes.route('/audio/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio = request.files['audio']

    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)

        # Log the file details for debugging
        print(f"Received file: {filename}, Type: {audio.mimetype}, Size: {len(audio.read())} bytes")

        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        audio.seek(0)  # Reset file pointer to the beginning
        audio.save(file_path)

        # Process the audio file (Transcription, Vectorization, etc.)
        try:
            # Here you would process the audio file, transcribe it, vectorize it, etc.
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
