"""
Kafka producer module for publishing stock data.
"""
import json
import os
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

class StockDataProducer:
    """Kafka producer for stock market data."""
    
    def __init__(self):
        """Initialize the Kafka producer."""
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = os.getenv('KAFKA_TOPIC', 'market_data')
        
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8')
        )
    
    def publish_stock_data(self, symbol: str, data: dict):
        """
        Publish stock data to Kafka topic.
        
        Args:
            symbol: Stock symbol
            data: Stock data dictionary
        """
        try:
            # Add timestamp for when the data was published
            data['published_at'] = datetime.utcnow().isoformat()
            
            # Use symbol as the key for partitioning
            future = self.producer.send(
                topic=self.topic,
                key=symbol,
                value=data
            )
            
            # Wait for the message to be delivered
            future.get(timeout=10)
            print(f"Published data for {symbol} to Kafka")
            
        except Exception as e:
            print(f"Error publishing data to Kafka: {str(e)}")
    
    def close(self):
        """Close the Kafka producer."""
        self.producer.close() 