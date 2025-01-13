"""
Data validation utilities.
"""
from datetime import datetime
from typing import Dict, Any, Optional

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_stock_data(data: Dict[str, Any]) -> Optional[str]:
    """
    Validate stock market data.
    
    Args:
        data: Dictionary containing stock data
        
    Returns:
        Optional[str]: Error message if validation fails, None if successful
        
    Raises:
        ValidationError: If data is invalid
    """
    required_fields = [
        'timestamp',
        'open_price',
        'high_price',
        'low_price',
        'close_price',
        'volume'
    ]
    
    # Check for required fields
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    
    try:
        # Validate timestamp
        datetime.fromisoformat(data['timestamp'])
        
        # Validate numeric fields
        prices = [
            float(data['open_price']),
            float(data['high_price']),
            float(data['low_price']),
            float(data['close_price'])
        ]
        
        # Validate price relationships
        if not (min(prices) > 0):  # All prices should be positive
            return "Invalid price values: prices must be positive"
            
        if not (float(data['high_price']) >= max(float(data['open_price']), float(data['close_price']))):
            return "Invalid price values: high price must be >= open and close prices"
            
        if not (float(data['low_price']) <= min(float(data['open_price']), float(data['close_price']))):
            return "Invalid price values: low price must be <= open and close prices"
        
        # Validate volume
        volume = int(data['volume'])
        if volume < 0:
            return "Invalid volume: must be non-negative"
            
    except ValueError as e:
        return f"Invalid numeric value: {str(e)}"
    except Exception as e:
        return f"Validation error: {str(e)}"
    
    return None  # Validation successful

def validate_symbol(symbol: str) -> bool:
    """
    Validate stock symbol format.
    
    Args:
        symbol: Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not symbol:
        return False
    
    # Basic symbol validation (can be extended based on requirements)
    return (
        len(symbol) >= 1 
        and len(symbol) <= 10 
        and symbol.isalpha()
        and symbol.isupper()
    ) 