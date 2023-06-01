import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_uri = os.getenv("DB_URI")
jwt_secret = os.getenv("JWT_SECRET_KEY")


JWT_SECRET_KEY = jwt_secret
DATABASE_URI = db_uri
# urlAddresses = ['http://127.0.0.1:5001', 'http://127.0.0.1:5002', 'http://127.0.0.1:5003']

