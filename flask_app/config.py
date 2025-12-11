# MySQL Database Configuration
# Cập nhật thông tin này theo MySQL server của bạn

MYSQL_CONFIG = {
    'host': 'localhost',      # Địa chỉ MySQL server
    'user': 'root',          # Username MySQL
    'password': '123456',    # Password MySQL (THAY ĐỔI NÀY!)
    'database': 'samsum_db', # Tên database
    'port': 3306,            # Port MySQL (mặc định 3306)
    'charset': 'utf8mb4',
    'autocommit': True
}

# Flask Secret Key
SECRET_KEY = 'your-secret-key-here-change-in-production'

# SQLite path (để migrate dữ liệu) - relative to project root
import os
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'Samsum', 'data', 'samsum.db')
