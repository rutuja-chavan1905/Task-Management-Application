# routes/auth_routes.py
# ============================================
# Authentication Routes
# Handles Register, Login, and Profile
# ============================================

from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
import datetime
from models import create_user, get_user_by_email, get_user_by_id
from config import Config

# Blueprint groups related routes together
auth_bp = Blueprint("auth", __name__)
bcrypt  = Bcrypt()


# --------------------------------------------------
# Helper: Decode JWT token from request header
# --------------------------------------------------
def get_current_user():
    """
    Reads the Authorization header, verifies the JWT token,
    and returns the user_id if valid. Returns None if invalid.
    """
    auth_header = request.headers.get("Authorization", "")

    # Header format: "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]

    try:
        # Decode the token using our secret key
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None   # Token has expired
    except jwt.InvalidTokenError:
        return None   # Token is invalid


# --------------------------------------------------
# POST /register
# Create a new user account
# --------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validate required fields
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    # Check if email is already registered
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "Email is already registered"}), 409

    # Hash the password before saving (never store plain text passwords!)
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    # Save user to database
    user_id = create_user(name, email, hashed_pw)

    return jsonify({
        "message": "Registration successful! Please login.",
        "user_id": user_id
    }), 201


# --------------------------------------------------
# POST /login
# Authenticate user and return a JWT token
# --------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = get_user_by_email(email)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    # Compare provided password with stored hash
    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token valid for 24 hours
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXPIRY_SECONDS)
    token  = jwt.encode(
        {"user_id": user["id"], "exp": expiry},
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token"  : token,
        "user"   : {
            "id"   : user["id"],
            "name" : user["name"],
            "email": user["email"]
        }
    }), 200


# --------------------------------------------------
# GET /profile
# Get logged-in user's profile (requires token)
# --------------------------------------------------
@auth_bp.route("/profile", methods=["GET"])
def profile():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized. Please login first."}), 401

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Convert datetime to string for JSON
    if user.get("created_at"):
        user["created_at"] = str(user["created_at"])

    return jsonify({"user": user}), 200
