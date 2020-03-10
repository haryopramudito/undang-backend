from flask import Flask
from flask_pymongo import PyMongo
import urllib.parse

apps = Flask(__name__)
apps.config["MONGO_URI"] = "mongodb://undang:"+urllib.parse.quote("undang@2020")+"@localhost:27017/undang"
mongo = PyMongo(apps)