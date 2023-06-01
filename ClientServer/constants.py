import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DATABASE_URI = os.getenv("DB_URI")
MANAGEMENT_NODE_URL = os.getenv("MANAGEMENT_NODE_URL")


