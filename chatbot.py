# chatbot.py

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pinecone_tools import read_vector  

# Load model and embeddings
llm = ChatGroq(model="llama3-8b-8192")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Set up RAG prompt and chain
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs, context):
    formatted = []
    for doc in docs:
        metadata = doc.get('metadata', {})
        # Combine content, metadata, and context in the formatted string
        formatted_doc = f"Context: {context}\n Retrieved_data: {metadata}"
        formatted.append(formatted_doc)
    
    return "\n\n".join(formatted)



# Define the RAG chain
rag_chain = (
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Function to retrieve from Pinecone and generate a response
def generate_response(question):

    print(f"Question: {question}")
    question_embedding = embeddings.embed_query(question)  # Using embed_query for single query embedding
    print(f"Question embedding: {question_embedding}")

    # Step 2: Query Pinecone for similar documents
    results = read_vector(question_embedding)

    retrieved_docs = results['matches'] if results else []

    context="""You are an advanced memory assistant designed to help users retrieve and interact with their stored memories. Your primary task is to accurately answer the user’s queries based on their past recorded experiences, which include audio and visual data stored in the Memopin system. You will retrieve relevant information from the vector database and respond in a clear, concise, and contextually appropriate manner.

1. Understand the User Query: Analyze the user’s request carefully to identify the most relevant memories or data points. The user may ask about past events, such as what they were doing at a specific time or any details related to a particular moment.

2. Contextual Relevance: If the user asks for information about a past event, retrieve and generate a response based on the context, including date, time, emotions, location, or any other factors the system can extract from the stored data.

3. Accuracy: Ensure that the retrieved data matches the user's request precisely. If the information is incomplete, mention that some details may be missing or require further clarification.

4. Friendly & Reassuring Tone: Respond in a friendly, reassuring manner. Remember that the user may rely on you to help them recall important or sentimental moments. Your tone should be comforting and empathetic, especially when handling sensitive or emotionally significant memories.

5. Memory Limitations: If the requested information isn't available or the memory is incomplete, inform the user in a polite and helpful manner, offering suggestions for refining the query or requesting additional details.

6. Support for Future Events: If the user asks about a future event, offer to set reminders or provide suggestions based on their past preferences. 

7. Provide Personalized Feedback: If the user seeks to review or update their memory records, offer them an easy-to-understand summary of their stored data and suggest actions they can take to add or modify their memories.

8. Handle Emotional Queries with Care: When dealing with sensitive memories, such as anniversaries or personal milestones, respond with added empathy, offering encouragement and validating the user’s emotions.

9. Inform the User of Available Features: When the user asks about specific functionalities of Memopin, such as adding memories, reviewing past experiences, or asking about specific dates, provide detailed explanations of how the system works and how they can use it effectively.

Now, proceed to assist the user with their request."""

    formatted_docs = format_docs(retrieved_docs, context)
    # print(f"Formatted docs:🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 {formatted_docs}")
   

    response_generator = rag_chain.invoke({"context": formatted_docs, "question": question})
    print(f"Response text: {response_generator}")

    return response_generator
