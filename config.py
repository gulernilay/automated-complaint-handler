from dotenv import load_dotenv
import os

load_dotenv()

WATCH_FOLDER = os.getenv("WATCH_FOLDER")
EXCEL_FILE = os.getenv("EXCEL_FILE")
TARGET_TABLE = os.getenv("TARGET_TABLE")

SQL_DRIVER = os.getenv("SQL_DRIVER")
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER").split(",")

LOG_FILE = os.getenv("LOG_FILE")
DELAY_MINUTES = int(os.getenv("DELAY_MINUTES", 1))