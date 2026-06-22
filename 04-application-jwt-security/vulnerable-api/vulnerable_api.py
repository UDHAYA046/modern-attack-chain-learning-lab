import base64
import hashlib
import hmac
import json
import time
from pathlib import Path

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
KEY_DIR = BASE_DIR / "keys"

PRIVATE_KEY = (KEY_DIR / "private.pem").read_text(encoding="utf-8")
PUBLIC_KEY = (KEY_DIR / "public.pem").read_text(encoding="utf-8")

WEAK_HS256_SECRET = "secret123"
ISSUER = "lab4-vulnerable-api"
AUDIENCE = "lab4-users"


def b64url_decode(data):
    data += "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data.encode())


def b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def extract_bearer_token():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    return auth_header.replace("Bearer ", "").strip()


def verify_hs256_manually(token, secret):
    header_b64, payload_b64, signature_b64 = token.split(".")

    signing_input = f"{header_b64}.{payload_b64}".encode()

    expected_signature = hmac.new(
        secret,
        signing_input,
        hashlib.sha256
    ).digest()

    expected_b64 = b64url_encode(expected_signature)

    if not hmac.compare_digest(expected_b64, signature_b64):
        raise ValueError("Invalid HS256 signature")

    return json.loads(b64url_decode(payload_b64))


def vulnerable_decode(token):
    header = jwt.get_unverified_header(token)
    algorithm = header.get("alg")

    if algorithm == "none":
        parts = token.split(".")
        return json.loads(b64url_decode(parts[1]))

    if algorithm == "HS256":
        try:
            return verify_hs256_manually(
                token,
                WEAK_HS256_SECRET.encode()
            )
        except Exception:
            return verify_hs256_manually(
                token,
                PUBLIC_KEY.encode()
            )

    if algorithm == "RS256":
        return jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
                "verify_iss": False
            }
        )

    raise ValueError("Unsupported algorithm")


def create_token(username, role, algorithm):
    payload = {
        "username": username,
        "role": role,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": int(time.time()),
        "nbf": int(time.time()),
        "exp": int(time.time()) + 900
    }

    if algorithm == "HS256":
        return jwt.encode(
            payload,
            WEAK_HS256_SECRET,
            algorithm="HS256"
        )

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256"
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Lab 4 Vulnerable JWT API is running",
        "endpoints": ["/login", "/profile", "/admin"]
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "alice")
    role = data.get("role", "user")
    algorithm = data.get("algorithm", "RS256")

    token = create_token(username, role, algorithm)

    return jsonify({
        "message": "Token issued",
        "algorithm": algorithm,
        "username": username,
        "role": role,
        "token": token
    })


@app.route("/profile")
def profile():
    token = extract_bearer_token()

    if not token:
        return jsonify({"error": "Missing bearer token"}), 401

    try:
        decoded = vulnerable_decode(token)

        return jsonify({
            "message": "Profile access granted",
            "user": decoded
        })

    except Exception as error:
        return jsonify({
            "error": "Invalid token",
            "details": str(error)
        }), 401


@app.route("/admin")
def admin():
    token = extract_bearer_token()

    if not token:
        return jsonify({"error": "Missing bearer token"}), 401

    try:
        decoded = vulnerable_decode(token)

        if decoded.get("role") == "admin":
            return jsonify({
                "message": "Admin access granted",
                "user": decoded
            })

        return jsonify({
            "error": "Admin access denied",
            "user": decoded
        }), 403

    except Exception as error:
        return jsonify({
            "error": "Invalid token",
            "details": str(error)
        }), 401


if __name__ == "__main__":
    app.run(debug=True, port=5000)