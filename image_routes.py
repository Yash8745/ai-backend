from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from image_description_main import describe_image  # Import the description generation function
from utils import SentenceTransformer
from pinecone_tools import create_vector

# Load the SentenceTransformer model (customize as needed)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

image_routes = Blueprint('image_routes', __name__)

# Set up the upload folder path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image_uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload folder at: {UPLOAD_FOLDER}")

# Function to check allowed file types
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        print(f"File '{filename}' is of an allowed type.")
        return True
    else:
        print(f"File '{filename}' is not an allowed type.")
        return False

@image_routes.route('/image/upload', methods=['POST'])
def upload_image():
    # Check if the request has the 'image' file part
    if 'image' not in request.files:
        print("No image file part found in the request.")
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']

    # Check if the image file is valid
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"Received image file '{filename}', saving to: {file_path}")

        try:
            # Save the image file to the uploads folder
            image.save(file_path)
            print(f"Image '{filename}' saved successfully.")

            # Step 1: Generate image description
            print("Generating image description...")
            description = describe_image(file_path)
            print(f"Image description: {description}")

            # Step 2: Generate an embedding for the description
            print("Generating embedding for the description...")
            embedding = embedding_model.encode(description).tolist()  # Convert to list of floats
            print(f"Generated embedding for the description: {embedding[:5]}... (truncated for display)")

            # Step 3: Store the vector in Pinecone
            print("Storing vector in Pinecone...")
            create_vector(filename, embedding)
            print(f"Vector stored successfully for filename: {filename}")

            response = {
                'message': 'Image processed and vector stored successfully',
                'description': description,
                'filename': filename
            }
            return jsonify(response)

        except Exception as e:
            print(f"Error during image processing: {str(e)}")
            return jsonify({'error': str(e)}), 500
    else:
        print("Invalid file type provided.")
        return jsonify({'error': 'Invalid file type. Only .jpg, .jpeg, .png, .gif are allowed'}), 400
