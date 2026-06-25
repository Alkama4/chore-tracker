import os
from dotenv import load_dotenv
load_dotenv()

db_path = os.environ.get("DB_PATH", "chore_tracker.db")

DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
