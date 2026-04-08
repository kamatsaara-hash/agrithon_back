from pymongo import MongoClient

# 🔐 MongoDB Atlas Connection URL
MONGO_URL = "mongodb+srv://web:YLVC8wjgLOfzERQ7@cluster0.gitqnpn.mongodb.net/users?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URL)

# Select Database
db = client["agri_db"]

# Collections
users = db["users"]
crops = db["crops"]
orders = db["orders"]  # optional (you had it earlier)