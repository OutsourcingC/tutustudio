from flask import jsonify
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTExtendedException


def validate_jwt_from_cookie(access_token: str) -> tuple[..., ...]:
    if not access_token:
        return None, 401, jsonify({"msg": "Missing access token"})

    try:
        decode_token(access_token)
        return True, 200, jsonify({"msg": "success"})
    except JWTExtendedException:
        return None, 401, jsonify({"msg": "Invalid access token"})
