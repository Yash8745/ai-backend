from flask import Blueprint, request, jsonify,g
import pinecone
from config import user_dict

user_routes = Blueprint('user_routes', __name__)

# user_dict = {}

@user_routes.route('/user', methods=['POST'])
def create_namespace():
    try:
        data = request.get_json()
        # user_dict=data
        user_dict.update(data)
        return jsonify({'message': 'Got the id!!'})
    except Exception as e:
        print(f"Error file user_routes: {e}")
        return jsonify({'message': 'Error didnt get id!!'})

    