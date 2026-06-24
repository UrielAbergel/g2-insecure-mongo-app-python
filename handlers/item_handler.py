# handlers/item_handler.py

import json
import uuid

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from flask import jsonify, request
from pymongo.collection import Collection


def handle_get_item(collection: Collection):
    """Handle GET /items."""
    id_raw = request.args.get("id")
    if not id_raw:
        return jsonify(error="Missing required query parameter: id"), 404

    try:
        parsed_id = json.loads(
            id_raw if id_raw.startswith(("{", "[", '"')) else f'"{id_raw}"'
        )
        filter_doc = {"id": parsed_id}
        results = list(collection.find(filter_doc))

        if not results:
            return jsonify(error="No documents found"), 404

        for doc in results:
            doc["_id"] = str(doc["_id"])

        return jsonify(results), 200
    except Exception as e:
        return jsonify(error="Invalid query parameter format", detail=str(e)), 400


def handle_post_item(collection: Collection):
    """Handle POST /items."""
    try:
        data = request.get_json(force=True)
        item_id = str(uuid.uuid4())

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
        signature = private_key.sign(
            item_id.encode(), padding.PKCS1v15(), hashes.SHA1()
        )

        data["id"] = item_id
        data["sig"] = signature.hex()

        result = collection.insert_one(data)
        data["_id"] = str(result.inserted_id)

        return jsonify(data), 201
    except Exception as e:
        return jsonify(error="Invalid request", detail=str(e)), 400
