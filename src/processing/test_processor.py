"""
Test data processing functionality.
"""
import os
import sys
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_processing():
    """Test basic data processing functionality."""
    try:
        logger.info("Creating test database connection...")
        engine = create_engine('postgresql://postgres:postgres@localhost:5432/financial_data')
        
        # Create test data
        logger.info("Creating test data...")
        test_data = pd.DataFrame({
            'symbol': ['AAPL', 'AAPL', 'AAPL', 'MSFT', 'MSFT'],
            'timestamp': [
                datetime.now(),
                datetime.now() + timedelta(minutes=1),
                datetime.now() + timedelta(minutes=2),
                datetime.now(),
                datetime.now() + timedelta(minutes=1)
            ],
            'open_price': [150.0, 151.0, 152.0, 250.0, 251.0],
            'close_price': [150.0, 151.0, 152.0, 250.0, 251.0],
            'high_price': [152.0, 153.0, 154.0, 252.0, 253.0],
            'low_price': [149.0, 150.0, 151.0, 249.0, 250.0],
            'volume': [1000, 1100, 1200, 2000, 2100]
        })
        
        # Write test data to database
        logger.info("Writing test data to database...")
        test_data.to_sql('stock_prices', engine, if_exists='append', index=False)
        
        # Test window calculations
        logger.info("Testing window calculations...")
        window_duration = '5min'
        grouped = test_data.groupby([
            'symbol',
            pd.Grouper(key='timestamp', freq=window_duration)
        ]).agg({
            'close_price': 'mean',
            'high_price': 'max',
            'low_price': 'min',
            'volume': 'sum',
        }).reset_index()
        
        # Add trade count as length of each group
        grouped['trade_count'] = test_data.groupby([
            'symbol',
            pd.Grouper(key='timestamp', freq=window_duration)
        ]).size().values
        
        # Verify results
        logger.info("Verifying results...")
        assert len(grouped) > 0, "No grouped results generated"
        assert 'close_price' in grouped.columns, "Missing average price calculation"
        assert 'high_price' in grouped.columns, "Missing max price calculation"
        assert 'low_price' in grouped.columns, "Missing min price calculation"
        assert 'trade_count' in grouped.columns, "Missing trade count calculation"
        
        logger.info("All tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error("Test failed!", exc_info=True)
        return False
    finally:
        # Clean up test data
        if 'engine' in locals():
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM stock_prices WHERE symbol IN ('AAPL', 'MSFT')"))
                conn.commit()

if __name__ == "__main__":
    success = test_processing()
    sys.exit(0 if success else 1) 