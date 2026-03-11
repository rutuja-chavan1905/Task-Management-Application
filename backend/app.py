# app.py
# ============================================
# Smart Task & Productivity Manager
# Main Flask Application Entry Point
# ============================================

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from routes.auth_routes import auth_bp, bcrypt
from routes.task_routes import task_bp
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Enable CORS so the React frontend can call this API
# In production, replace "*" with your frontend URL
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Bcrypt with the app
bcrypt.init_app(app)

# Register route blueprints (groups of related routes)
app.register_blueprint(auth_bp)   # /register, /login, /profile
app.register_blueprint(task_bp)   # /tasks, /dashboard


# --------------------------------------------------
# Root endpoint — just to confirm the API is running
# --------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return {"message": "Smart Task Manager API is running!"}, 200


# --------------------------------------------------
# Run the development server
# --------------------------------------------------
if __name__ == "__main__":
    # debug=True enables auto-reload and error details
    # Remove debug=True in production!
    app.run(debug=True, host="0.0.0.0", port=5000)
