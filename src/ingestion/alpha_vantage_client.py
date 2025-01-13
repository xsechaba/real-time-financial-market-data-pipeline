"""
Alpha Vantage API client for fetching financial market data.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageClient:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = 'https://www.alphavantage.co/query'
        
    def get_stock_data(self, symbol: str, function: str = 'TIME_SERIES_INTRADAY', interval: str = '1min'):
        """
        Fetch stock data from Alpha Vantage API.
        
        Args:
            symbol: Stock symbol (e.g., 'IBM')
            function: API function to call
            interval: Time interval for data points
            
        Returns:
            dict: JSON response from the API
        """
        params = {
            'function': function,
            'symbol': symbol,
            'interval': interval,
            'apikey': self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json() 