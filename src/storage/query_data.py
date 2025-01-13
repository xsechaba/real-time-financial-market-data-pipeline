"""
Script to query and display stored stock data.
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from database import get_db_session
from models import StockPrice

def query_latest_data():
    """Query and display the latest stock data for each symbol."""
    try:
        session = get_db_session()
        
        # Get unique symbols
        symbols_query = select(StockPrice.symbol).distinct()
        symbols = [row[0] for row in session.execute(symbols_query)]
        
        print(f"\nFound data for {len(symbols)} symbols")
        print("-" * 50)
        
        for symbol in symbols:
            # Get the latest entry for this symbol
            query = (select(StockPrice)
                    .filter(StockPrice.symbol == symbol)
                    .order_by(StockPrice.timestamp.desc())
                    .limit(1))
            
            result = session.execute(query).scalar()
            
            if result:
                print(f"\nLatest data for {symbol}:")
                print(f"Timestamp: {result.timestamp}")
                print(f"Open: ${result.open_price:.2f}")
                print(f"High: ${result.high_price:.2f}")
                print(f"Low: ${result.low_price:.2f}")
                print(f"Close: ${result.close_price:.2f}")
                print(f"Volume: {result.volume}")
            
            # Get count of entries for this symbol
            count_query = select(StockPrice).filter(StockPrice.symbol == symbol)
            entry_count = len(list(session.execute(count_query)))
            print(f"Total entries: {entry_count}")
            
    except Exception as e:
        print(f"Error querying data: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    query_latest_data() 