from flask import Flask
from flask_pymongo import PyMongo

apps = Flask(__name__)
apps.config["MONGO_URI"] = "mongodb://localhost:27017/undang"
mongo = PyMongo(apps)