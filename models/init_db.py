# models/init_db.py

from pymongo import MongoClient

from config import DB_NAME, MONGO_URI

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Use (or create) the database
db = client.get_database(DB_NAME)

# Expose collections
items_collection = db["items"]
users_collection = db["users"]
