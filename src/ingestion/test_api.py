"""
Test Alpha Vantage API integration.
"""
from alpha_vantage_client import AlphaVantageClient

def test_api():
    """Test the Alpha Vantage API connection and data retrieval."""
    try:
        # Initialize the client
        client = AlphaVantageClient()
        
        # Test with a simple stock query (using IBM as an example)
        print("Fetching IBM stock data...")
        data = client.get_stock_data('IBM')
        
        # Print the response structure
        print("\nAPI Response structure:")
        for key in data.keys():
            print(f"- {key}")
            
        # If we have time series data, print the latest entry
        if "Time Series (1min)" in data:
            latest_time = list(data["Time Series (1min)"].keys())[0]
            latest_data = data["Time Series (1min)"][latest_time]
            print(f"\nLatest data point ({latest_time}):")
            for key, value in latest_data.items():
                print(f"{key}: {value}")
                
    except Exception as e:
        print(f"Error testing API: {str(e)}")

if __name__ == "__main__":
    test_api() 