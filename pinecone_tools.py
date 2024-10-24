import pinecone
from config import PINECONE_API_KEY

pinecone_instance = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment="us-east1-gcp")
index_name = 'memopin'

if index_name not in pinecone_instance.list_indexes().names():
    pinecone_instance.create_index(name=index_name, dimension=384, metric='cosine')

index = pinecone_instance.Index(index_name)

def create_vector(vector_id, embedding):
    index.upsert([(vector_id, embedding)])

def read_vector(vector_id):
    response = index.fetch(ids=[vector_id])
    return response.vectors.get(vector_id, None)

def update_vector(vector_id, new_embedding):
    index.upsert([(vector_id, new_embedding)])

def delete_vector(vector_id):
    index.delete(ids=[vector_id])
