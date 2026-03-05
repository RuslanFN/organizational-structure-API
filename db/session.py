from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import getenv
from typing import Iteratorte
load_dotenv()

db_driver = 'postgresql+psycopg2'
db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')
db_name = getenv('DB_NAME')

conn = f'{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(conn, echo=True)
session_maker = sessionmaker(bind=engine)

def get_session() -> Iteratorte[Session]:
    with session_maker() as session:
        yield session
