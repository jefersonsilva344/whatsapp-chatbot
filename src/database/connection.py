import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
DATABASE = str(DATA_DIR / "chatbot.db")


class DatabaseConnection:

    def __init__(self):

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DATABASE,
            timeout=10,
            check_same_thread=False
        )

        self.connection.execute(
            "PRAGMA journal_mode=WAL;"
        )

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()