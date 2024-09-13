from flask import request, jsonify, session, render_template
from flask_jwt_extended import decode_token
from functools import wraps

def jwt_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.cookies.get('auth')
        if not auth_header:
            return jsonify({"message": "Missing Authorization Header"}), 401

        token = auth_header
        try:
            decoded_token = decode_token(token)
            user_identity = decoded_token['sub']
            session['username'] = user_identity
        except Exception as e:
            return jsonify({"message": f"Invalid or expired token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorator
