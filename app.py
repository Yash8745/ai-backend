from flask import Flask, jsonify
from flask_cors import CORS
from audio_routes import audio_routes
from image_routes import image_routes
from model_routes import model_routes
app = Flask(__name__)
CORS(app)

# Define a root route
@app.route('/')
def home():
    print("Root route accessed")
    return jsonify({"message": "Welcome to the Audio Processing API!"})

# Register the audio blueprint
app.register_blueprint(audio_routes, url_prefix='/')
app.register_blueprint(image_routes, url_prefix='/')
app.register_blueprint(model_routes, url_prefix='/')

if __name__ == "__main__":
    print("Starting Flask app on port 5000...") 
    app.run(port=5000, debug=True)
