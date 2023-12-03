import os

from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# List of variables to check
variables = [
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_DATABASE",
    "CACHE_HOST",
    "CACHE_PORT",
]

# Check if any of the variables are missing in the environment
if any(variable not in os.environ for variable in variables):
    from dotenv import load_dotenv

    load_dotenv()

# These should now point to the ProxySQL service
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 6033)  # Port changed to ProxySQL's client port
DB_USER = os.getenv("DB_USER", "stud")
DB_PASSWORD = os.getenv("DB_PASSWORD", "stud")
DB_DATABASE = os.getenv("DB_DATABASE", "archdb")

# Redis configuration
REDIS_HOST = os.getenv("CACHE_HOST", "localhost")
REDIS_PORT = os.getenv("CACHE_PORT", 6379)
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
