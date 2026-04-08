from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["agri_db"]

users = db["users"]
crops = db["crops"]
orders = db["orders"]