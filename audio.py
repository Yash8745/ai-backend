import whisper # type: ignore

# Load the Whisper model
whisper_model = whisper.load_model("base")

def transcribe_audio(audio_path):
    try:
        # Transcribe the audio using Whisper
        print(f"Transcribing audio from: {audio_path}")  # Debugging output
        result = whisper_model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise Exception("Audio transcription failed.")
