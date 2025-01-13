"""
Test database connectivity.
"""
from database import create_db_engine
from sqlalchemy import text

def test_connection():
    """Test the database connection."""
    try:
        # Create engine
        engine = create_db_engine()
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            
            # Test if we can create a new connection
            connection.execute(text("SELECT current_timestamp"))
            print("Query execution successful!")
            
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    test_connection() 