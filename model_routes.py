from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio import transcribe_audio
from chatbot import generate_response  # Import generate_response to handle retrieval + response generation
from flask import Response
import json

# Set up embedding model and Flask Blueprint
model_routes = Blueprint('model_routes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'webm'}

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@model_routes.route('/model/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']

    # Validate and save audio file
    if audio and allowed_file(audio.filename):
        filename = secure_filename(audio.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        audio.save(file_path)

        try:
            # Step 1: Transcribe the audio to get the user's question
            transcription = transcribe_audio(file_path)
            print(f"Transcription result: {transcription}")  # Debugging output

            # Step 2: Generate a response using the RAG model (retrieval + response generation in chatbot.py)
            response_text = generate_response(transcription)  # This now handles retrieval and response generation
            print(f"-------------------------------- I am here _________________________")  # Debugging output

            response = {
                'message': 'Audio processed and vector stored successfully',
                'filename': response_text
            }
            return jsonify(response)

        except Exception as e:
            print(f"Error processing audio: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type. Allowed types are: .wav, .mp3, .ogg, .flac, .m4a, .webm'}), 400
