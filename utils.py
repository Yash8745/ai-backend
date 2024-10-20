from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    return text.strip().lower()

def get_text_embedding(text):
    cleaned_text = preprocess_text(text)
    return sentence_model.encode(cleaned_text)
