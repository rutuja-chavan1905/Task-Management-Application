# config.py
# ============================================
# Application Configuration
# Contains database and app settings
# ============================================

class Config:
    # ----- Database Settings -----
    # Update these values to match your MySQL setup
    MYSQL_HOST     = "localhost"
    MYSQL_USER     = "root"         # Your MySQL username
    MYSQL_PASSWORD = "system"             # Your MySQL password
    MYSQL_DB       = "smart_task_db"

    # ----- Security -----
    # Secret key used to sign JWT tokens — change this in production!
    SECRET_KEY = "college_project_secret_key_2025"

    # ----- JWT Token Expiry -----
    # Token expires after 24 hours (in seconds)
    JWT_EXPIRY_SECONDS = 86400
