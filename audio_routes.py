from flask import Blueprint, request, jsonify
from audio import transcribe_audio  # Adjust the import based on your file structure
from pinecone_tools import create_vector  # Adjust the import based on your file structure
from utils import get_text_embedding  # Adjust the import based on your file structure
import os

audio_bp = Blueprint('audio', __name__)

UPLOAD_DIRECTORY = "./uploads"  # Define the upload directory

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    print(f"Upload directory created at: {UPLOAD_DIRECTORY}")  # Debugging output

@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    print("Upload route accessed")  # Debugging output

    if 'audio' not in request.files:
        print("No audio file provided.")  # Debugging output
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join(UPLOAD_DIRECTORY, audio_file.filename)  # Save the audio file

    audio_file.save(audio_path)  # Save the uploaded audio file
    print(f"Audio saved at: {audio_path}")  # Debugging output

    # Transcribe audio to text
    transcribed_text = transcribe_audio(audio_path)
    print(f"Transcribed Text: {transcribed_text}")  # Debugging output

    # Convert text to vector and store in Pinecone
    embedding = get_text_embedding(transcribed_text)
    vector_id = audio_file.filename  # Use filename as the vector ID
    create_vector(vector_id, embedding)

    print("Audio processed and vector stored successfully.")  # Debugging output
    return jsonify({"message": "Audio processed and vector stored successfully."}), 200