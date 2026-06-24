# config.py

import os

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_URI = f"mongodb://root:example@{MONGO_HOST}:27017/mydb?authSource=admin"
DB_NAME = "mydb"

JWT_SECRET = "BCV$9zjrZ3IPyAFwh*7N66%mx@)W++He!"
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 30
