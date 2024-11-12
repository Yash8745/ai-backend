from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio import transcribe_audio
from pinecone_tools import create_vector
from utils import SentenceTransformer  # Assuming you use SentenceTransformer for embeddings

# Load the SentenceTransformer model (customize as needed)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

audio_routes = Blueprint('audio_routes', __name__)

# Define the uploads directory using an absolute path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'webm'}  # Allow webm extension

# Check if the uploads folder exists or create it
if not os.path.exists(UPLOAD_FOLDER):
    print(f"Uploads folder does not exist, creating it at {UPLOAD_FOLDER}")
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print(f"Uploads folder created at: {UPLOAD_FOLDER}")
    except OSError as e:
        print(f"Error creating uploads folder: {e}")

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_routes.route('/audio/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']

    # Check if the audio file is valid
    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        print(f"Received file: {filename}, Size: {audio.content_length} bytes")  # Log the received file

        try:
            # Save the audio file to the uploads directory
            audio.save(file_path)
            print(f"Audio saved to {file_path}")  # Confirm file save

            # Step 1: Transcribe the audio
            transcription = transcribe_audio(file_path)
            print(f"Transcription result: {transcription}")  # Log transcription result

            # Step 2: Generate an embedding for the transcription
            embedding = embedding_model.encode(transcription).tolist()  # Convert to list of floats

            # Step 3: Store the vector in Pinecone
            vector_id = filename  # Using the filename as vector_id (you can modify this)
            create_vector(vector_id, embedding)

            response = {
                'message': 'Audio processed and vector stored successfully',
                'filename': filename
            }
            return jsonify(response)

        except Exception as e:
            print(f"Error processing audio: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only .wav, .mp3, .ogg, .flac, .m4a, .webm files are allowed'}), 400
