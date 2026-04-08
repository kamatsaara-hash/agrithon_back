import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Mongo URI from .env
MONGO_URL = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URL)

# Select Database
db = client["agri_db"]

# Collections
users = db["users"]
crops = db["crops"]
orders = db["orders"]