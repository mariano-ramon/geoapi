from geoapi import app
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/geoapi"
mongo = PyMongo(app)
