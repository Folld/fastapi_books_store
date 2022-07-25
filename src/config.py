from pathlib import Path

BASE_DIR = Path(__file__).parent
SQLITE_PATH = BASE_DIR / "sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///" + SQLITE_PATH.__str__()
