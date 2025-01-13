"""
Database connection and operations module.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL from environment variables."""
    return (f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

def create_db_engine():
    """Create and return a database engine."""
    return create_engine(get_database_url())

def get_db_session():
    """Create and return a database session."""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session() 