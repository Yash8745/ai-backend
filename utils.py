from sentence_transformers import SentenceTransformer # type: ignore

# Load the sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    # Preprocess the text (strip, lowercase)
    return text.strip().lower()

def get_text_embedding(text):
    try:
        # Preprocess the text and get the embedding
        cleaned_text = preprocess_text(text)
        print(f"Cleaned text: {cleaned_text}")  # Debugging output
        return sentence_model.encode(cleaned_text)
    except Exception as e:
        print(f"Error during embedding generation: {e}")
        raise Exception("Text embedding failed.")
