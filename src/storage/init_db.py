"""
Initialize the database schema.
"""
import os
import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, DateTime, Integer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL based on environment."""
    if os.environ.get('IN_DOCKER'):
        host = 'postgres'
    else:
        host = 'localhost'
    return f'postgresql://postgres:postgres@{host}:5432/financial_data'

def init_db():
    """Initialize database tables."""
    try:
        logger.info("Connecting to database...")
        engine = create_engine(get_database_url())
        metadata = MetaData()

        # Drop existing tables if they exist
        logger.info("Dropping existing tables...")
        metadata.reflect(bind=engine)
        metadata.drop_all(engine)
        
        # Clear metadata to prepare for new table definitions
        metadata = MetaData()

        # Stock prices table - raw data
        Table('stock_prices', metadata,
              Column('id', Integer, primary_key=True),
              Column('symbol', String(10), nullable=False),
              Column('timestamp', DateTime, nullable=False),
              Column('open_price', Float, nullable=False),
              Column('close_price', Float, nullable=False),
              Column('high_price', Float, nullable=False),
              Column('low_price', Float, nullable=False),
              Column('volume', Integer, nullable=False),
              Column('created_at', DateTime, nullable=False))

        # Stock analysis table - processed data
        Table('stock_analysis', metadata,
              Column('id', Integer, primary_key=True),
              Column('symbol', String(10), nullable=False),
              Column('window_start', DateTime, nullable=False),
              Column('window_end', DateTime, nullable=False),
              Column('avg_price', Float, nullable=False),
              Column('max_price', Float, nullable=False),
              Column('min_price', Float, nullable=False),
              Column('volume', Integer, nullable=False),
              Column('trade_count', Integer, nullable=False))

        logger.info("Creating tables...")
        metadata.create_all(engine)
        logger.info("Database initialization completed successfully!")

    except Exception as e:
        logger.error("Error initializing database", exc_info=True)
        raise

if __name__ == "__main__":
    init_db() 