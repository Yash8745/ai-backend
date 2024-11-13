# chatbot.py

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pinecone_tools import read_vector  # Import read_vector to fetch data from Pinecone
import time

# Load model and embeddings
llm = ChatGroq(model="llama3-8b-8192")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Set up RAG prompt and chain
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.get('content', doc) if isinstance(doc, dict) else doc for doc in docs)

# Define the RAG chain
rag_chain = (
    {"context": format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Function to retrieve from Pinecone and generate a response
def generate_response(question):
    # Step 1: Create an embedding for the question
    print(f"Question: {question}")
    question_embedding = embeddings.embed_query(question)  # Using embed_query for single query embedding
    print(f"Question embedding: {question_embedding}")

    # Step 2: Query Pinecone for similar documents
    results = read_vector(question_embedding)
    print(f"Results: {results}")
    retrieved_docs = results['matches'] if results else []
    print(f"Retrieved docs: {retrieved_docs}")
    # Step 3: Format retrieved documents for input to the RAG model
    formatted_docs = format_docs(retrieved_docs)
    print(f"Formatted docs: {formatted_docs}")
    # Step 4: Generate a response using the RAG model
    context="You are a helpfull bot. You have all the information you need to answer the question.My name is Yash. My teammate names are Ananya and rudransh. I ate breadstickes today.If i am having a headache you should recommend me crocin. Answer the question correctly if you don't know answer to any of question make things up. My best friend name is Shubham. I am wearing a blue shirt today. My Mentors are Dr. Ashish Sir and Dr. Deepti Chopra."
    response_generator = rag_chain.invoke({"context": formatted_docs, "question": question})
    print(f"Response text: {response_generator}")

    return response_generator
