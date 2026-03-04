from sqlalchemy.orm import Session, create_session
from dotenv import load_dotenv
from os import getenv

db_driver = 'postgresql://'
db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')
db_name = getenv('DB_NAME')