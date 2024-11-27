import pinecone # type: ignore
from config import PINECONE_API_KEY
# from routes.user_routes import user_dict
from config import user_dict

# Initialize Pinecone instance
pinecone_instance = pinecone.Pinecone(api_key=PINECONE_API_KEY, environment="us-east1-gcp")
index_name = 'memopin'

# Create the index if it doesn't exist
if index_name not in pinecone_instance.list_indexes().names():
    pinecone_instance.create_index(name=index_name, dimension=384, metric='cosine')

# Access the created index
index = pinecone_instance.Index(index_name)


def create_vector(vector_id, embedding, metadata):
    try:
        username = user_dict.get('username', '')
        uuid = user_dict.get('uuid', '')
        namespace = f"{username}_{uuid}" if username and uuid else "memopin" 
        print(f"-------------------:{namespace}")
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary")

        index.upsert([(vector_id, embedding, metadata)], namespace=namespace)

        print(f"Vector id: {vector_id}  successfull")
    except Exception as e:
        print(f"Error during vector creation: {e}")
        raise Exception("Vectorization failed.")

def read_vector(vector):
    try:
        username = user_dict.get('username', '')
        uuid = user_dict.get('uuid', '')
        namespace = f"{username}_{uuid}" if username and uuid else "memopin"
        response = index.query(
    vector=vector,
    top_k=3,
    include_values=True,
    include_metadata=True,
    namespace=namespace 
)
        return response
    except Exception as e:
        print(f"Error reading vector: {e}")
        raise Exception("Failed to read vector.")

def update_vector(vector_id, new_embedding):
    try:
        index.upsert([(vector_id, new_embedding)])
        print(f"Vector for {vector_id} updated successfully.")
    except Exception as e:
        print(f"Error updating vector: {e}")
        raise Exception("Failed to update vector.")

def delete_vector(vector_id):
    try:
        index.delete(ids=[vector_id])
        print(f"Vector for {vector_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting vector: {e}")
        raise Exception("Failed to delete vector.")
