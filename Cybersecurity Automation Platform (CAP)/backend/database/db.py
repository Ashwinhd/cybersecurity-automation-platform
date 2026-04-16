import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/cap_db")

try:
    # Initialize MongoDB Client
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_database()
    
    # Verify connection
    client.server_info()
    print("Connected to MongoDB successfully!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

def get_collection(collection_name):
    """
    Helper function to get a specific collection from the database.
    """
    if db is not None:
        return db[collection_name]
    return None

# Collections
users_collection = get_collection("users")
scans_collection = get_collection("scans")
alerts_collection = get_collection("alerts")
logs_collection = get_collection("logs")
