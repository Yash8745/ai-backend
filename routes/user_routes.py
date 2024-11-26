from flask import Blueprint, request, jsonify
import pinecone

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user', methods=['POST'])
def create_namespace():
    try:
        data = request.get_json()
        print(data)
        # namespace = data['namespace']
        # pinecone.create_index(namespace)
        return jsonify({'message': 'Namespace created successfully'})
    except Exception as e:
        print(f"Error file user_routes: {e}")
        return jsonify({'message': 'Error creating namespace'})

    