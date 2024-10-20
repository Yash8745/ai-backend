from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World Yash afadf!'