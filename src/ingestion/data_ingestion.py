"""
Data ingestion script to fetch stock data and store it in the database.
"""
import sys
import time
from datetime import datetime
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from ingestion.alpha_vantage_client import AlphaVantageClient
from storage.database import get_db_session
from storage.models import StockPrice

def ingest_stock_data(symbol: str):
    """
    Fetch stock data and store it in the database.
    
    Args:
        symbol: Stock symbol to fetch data for
    """
    try:
        # Initialize API client and get DB session
        client = AlphaVantageClient()
        session = get_db_session()
        
        print(f"Fetching data for {symbol}...")
        data = client.get_stock_data(symbol)
        
        # Process time series data
        time_series = data.get("Time Series (1min)", {})
        entries_processed = 0
        
        for timestamp_str, values in time_series.items():
            # Parse timestamp
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            
            # Create StockPrice entry
            stock_price = StockPrice(
                symbol=symbol,
                timestamp=timestamp,
                open_price=float(values["1. open"]),
                high_price=float(values["2. high"]),
                low_price=float(values["3. low"]),
                close_price=float(values["4. close"]),
                volume=int(values["5. volume"])
            )
            
            session.add(stock_price)
            entries_processed += 1
        
        # Commit the transaction
        session.commit()
        print(f"Successfully processed {entries_processed} entries for {symbol}")
        
    except Exception as e:
        print(f"Error ingesting data: {str(e)}")
        if 'session' in locals():
            session.rollback()
    finally:
        if 'session' in locals():
            session.close()

def main():
    """Main function to run the ingestion process."""
    symbols = ['IBM', 'AAPL', 'MSFT']  # Example symbols
    
    for symbol in symbols:
        ingest_stock_data(symbol)
        # Sleep to respect API rate limits
        time.sleep(15)  # Alpha Vantage free tier has a rate limit of 5 calls per minute

if __name__ == "__main__":
    main() 