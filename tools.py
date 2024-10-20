from .pinecone_tools import create_vector, read_vector, update_vector, delete_vector
from .chatbot import LangChainChatbot
from .audio import transcribe_audio
from .utils import get_text_embedding

def tool_create_vector():
    text = input("Enter the text to store: ")
    vector_id = input("Enter a unique vector ID: ")
    embedding = get_text_embedding(text)
    create_vector(vector_id, embedding)
    print(f"Vector {vector_id} stored in Pinecone.")

def tool_read_vector():
    vector_id = input("Enter the vector ID to read: ")
    vector = read_vector(vector_id)
    if vector:
        print(f"Vector {vector_id} fetched: {vector}")
    else:
        print(f"Vector {vector_id} not found in Pinecone.")

def tool_update_vector():
    vector_id = input("Enter the vector ID to update: ")
    new_text = input("Enter the new text: ")
    new_embedding = get_text_embedding(new_text)
    update_vector(vector_id, new_embedding)
    print(f"Vector {vector_id} updated in Pinecone.")

def tool_delete_vector():
    vector_id = input("Enter the vector ID to delete: ")
    delete_vector(vector_id)
    print(f"Vector {vector_id} deleted from Pinecone.")

def tool_chat():
    chatbot = LangChainChatbot()
    question = input("Ask a question: ")
    answer = chatbot.answer_question(question)
    print(f"Answer: {answer}")

def tool_upload_audio():
    audio_path = input("Enter the path to the audio file: ")
    if os.path.exists(audio_path):
        chatbot = LangChainChatbot()
        question = transcribe_audio(audio_path)
        print(f"Transcribed Question: {question}")
        answer = chatbot.answer_question(question)
        print(f"Answer: {answer}")
    else:
        print("Invalid file path. Please try again.")
