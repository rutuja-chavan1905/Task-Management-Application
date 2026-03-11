# database.py
# ============================================
# Database Connection Helper
# Creates and returns a MySQL connection
# ============================================

import mysql.connector
from config import Config

def get_connection():
    """
    Creates and returns a new MySQL database connection.
    Call this function wherever you need to run a query.
    """
    connection = mysql.connector.connect(
        host     = Config.MYSQL_HOST,
        user     = Config.MYSQL_USER,
        password = Config.MYSQL_PASSWORD,
        database = Config.MYSQL_DB
    )
    return connection
