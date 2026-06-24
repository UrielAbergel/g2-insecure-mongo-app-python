# config.py

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/mydb?authSource=admin"
DB_NAME = "mydb"

JWT_SECRET = "BCV$9zjrZ3IPyAFwh*7N66%mx@)W++He!"
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 30
