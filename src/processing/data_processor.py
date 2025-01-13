"""
Data processor for analyzing stock market data using Pandas.
"""
import os
import sys
import logging
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment variables."""
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    name = os.environ.get('DB_NAME', 'financial_data')
    user = os.environ.get('DB_USER', 'postgres')
    password = os.environ.get('DB_PASSWORD', 'postgres')
    
    return f'postgresql://{user}:{password}@{host}:{port}/{name}'

def process_stock_data():
    """Process stock data from PostgreSQL using Pandas."""
    try:
        logger.info("Connecting to PostgreSQL database...")
        engine = create_engine(get_database_url())
        
        # Read data in chunks to handle large datasets
        chunk_size = 100000
        chunks = []
        
        logger.info("Reading data from PostgreSQL...")
        for chunk in pd.read_sql_table(
            'stock_prices',
            engine,
            chunksize=chunk_size
        ):
            chunks.append(chunk)
        
        # Combine all chunks
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"Read {len(df)} rows from stock_prices table")
        
        # Convert timestamp to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Set the window duration
        window_duration = '5min'  # Using 'min' instead of 'T'
        
        logger.info("Calculating moving averages...")
        # Group by symbol and time window
        grouped = df.groupby([
            'symbol',
            pd.Grouper(key='timestamp', freq=window_duration)
        ]).agg({
            'close_price': 'mean',
            'high_price': 'max',
            'low_price': 'min',
            'volume': 'sum'
        }).reset_index()
        
        # Add trade count as length of each group
        grouped['trade_count'] = df.groupby([
            'symbol',
            pd.Grouper(key='timestamp', freq=window_duration)
        ]).size().values
        
        # Rename columns
        grouped.columns = [
            'symbol',
            'window_start',
            'avg_price',
            'max_price',
            'min_price',
            'volume',
            'trade_count'
        ]
        
        # Add window end time
        grouped['window_end'] = grouped['window_start'] + pd.Timedelta(minutes=5)
        
        logger.info(f"Generated {len(grouped)} aggregated records")
        
        # Write results back to PostgreSQL
        logger.info("Writing results back to PostgreSQL...")
        grouped.to_sql(
            'stock_analysis',
            engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=10000
        )
        
        logger.info("Data processing completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error processing stock data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting data processing script")
        logger.info(f"Using database URL: {get_database_url()}")
        success = process_stock_data()
        if success:
            logger.info("Script completed successfully")
            sys.exit(0)
        else:
            logger.error("Script failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed with error: {str(e)}")
        sys.exit(1) 