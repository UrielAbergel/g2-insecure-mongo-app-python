from flasgger import Swagger
from flask import Flask, jsonify, request

from handlers import auth_handler, item_handler
from models.init_db import items_collection
from services import user_service

app = Flask(__name__)

swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "InsecureMongoApp API",
            "description": "An intentionally insecure API using MongoDB and JWT for security training.",
            "version": "1.0",
        },
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header. Example: Bearer {token}",
            }
        },
    },
)


@app.route("/auth/token", methods=["POST"])
def auth_token():
    """
    Authenticate and get a JWT
    ---
    tags:
      - auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: JWT returned
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Invalid credentials
    """
    creds = request.get_json()
    username = creds.get("username")
    password = creds.get("password")

    if username and password and user_service.validate_user(username, password):
        role = user_service.get_user_role(username) or "reader"
        token = auth_handler.generate_token(username, role)
        return jsonify(token=token)

    return "", 401


@app.route("/auth/register", methods=["POST"])
def register():
    """
    Register a new user (admin only)
    ---
    tags:
      - auth
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
              role:
                type: string
                enum: [reader, writer]
    responses:
      200:
        description: User created successfully
      400:
        description: Missing fields
      401:
        description: Unauthorized (must be admin)
      409:
        description: User already exists
    """
    token = auth_handler.extract_token_from_header()
    decoded = auth_handler.validate_token(token)

    if not decoded or decoded.get("name") != "admin":
        return "", 401

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "reader")

    if not username or not password:
        return "", 400

    if not user_service.create_user(username, password, role):
        return "", 409

    return jsonify(message="User created")


@app.route("/items", methods=["GET"])
def get_items():
    """
    Retrieve item(s) by ID (requires reader+)
    ---
    tags:
      - items
    parameters:
      - name: id
        in: query
        required: true
        type: string
        description: Parsed ID (JSON-based; injectable)
    security:
      - BearerAuth: []
    responses:
      200:
        description: A list of items
      400:
        description: Invalid query format
      401:
        description: Unauthorized
      404:
        description: No items found
    """
    token = auth_handler.extract_token_from_header()
    decoded = auth_handler.validate_token(token)
    role = auth_handler.get_role_from_token(decoded)

    if role not in ["admin", "writer", "reader"]:
        return "", 401

    return item_handler.handle_get_item(items_collection)


@app.route("/items", methods=["POST"])
def post_item():
    """
    Insert a new item (requires writer+)
    ---
    tags:
      - items
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            description: Arbitrary data to store in MongoDB
    responses:
      201:
        description: Item created
      400:
        description: Invalid request
      401:
        description: Unauthorized
    """
    token = auth_handler.extract_token_from_header()
    decoded = auth_handler.validate_token(token)
    role = auth_handler.get_role_from_token(decoded)

    if role not in ["admin", "writer"]:
        return "", 401

    return item_handler.handle_post_item(items_collection)


def create_app():
    return app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
