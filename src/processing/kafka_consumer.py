"""
Kafka consumer module for processing streaming stock market data.
"""
import json
import os
import time
from datetime import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from dotenv import load_dotenv
from storage.database import get_db_session
from storage.models import StockPrice
from utils.logging_config import setup_logger
from utils.validation import validate_stock_data, validate_symbol

load_dotenv()

class StockDataConsumer:
    """Kafka consumer for processing stock market data."""
    
    def __init__(self):
        """Initialize the Kafka consumer."""
        self.logger = setup_logger('kafka_consumer')
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.topic = os.getenv('KAFKA_TOPIC', 'market_data')
        self.group_id = 'stock_data_processor'
        self.consumer = None
        self.connect()
    
    def connect(self):
        """Establish connection to Kafka."""
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset='latest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                key_deserializer=lambda x: x.decode('utf-8') if x else None,
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000
            )
            self.logger.info(f"Successfully connected to Kafka topic: {self.topic}")
        except Exception as e:
            self.logger.error(f"Error connecting to Kafka: {str(e)}", exc_info=True)
            raise
    
    def process_messages(self):
        """Process incoming messages from Kafka topic."""
        if not self.consumer:
            self.logger.error("No consumer connection available")
            return

        session = get_db_session()
        try:
            self.logger.info(f"Starting to consume messages from topic: {self.topic}")
            
            for message in self.consumer:
                try:
                    symbol = message.key
                    data = message.value
                    
                    if not validate_symbol(symbol):
                        self.logger.error(f"Invalid symbol received: {symbol}")
                        continue
                    
                    validation_error = validate_stock_data(data)
                    if validation_error:
                        self.logger.error(f"Invalid data received for {symbol}: {validation_error}")
                        continue
                    
                    self.logger.info(f"Received data for {symbol}:")
                    self.logger.info(f"Timestamp: {data.get('timestamp')}")
                    self.logger.info(f"Price: ${data.get('close_price')}")
                    
                    # Create and store StockPrice entry
                    stock_price = StockPrice(
                        symbol=symbol,
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        open_price=float(data['open_price']),
                        high_price=float(data['high_price']),
                        low_price=float(data['low_price']),
                        close_price=float(data['close_price']),
                        volume=int(data['volume'])
                    )
                    
                    session.add(stock_price)
                    session.commit()
                    self.logger.info(f"Successfully stored {symbol} data in database")
                    
                except Exception as e:
                    self.logger.error(f"Error processing message: {str(e)}", exc_info=True)
                    session.rollback()
                    
        except KafkaError as e:
            self.logger.error(f"Kafka error: {str(e)}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        finally:
            session.close()
    
    def close(self):
        """Close the Kafka consumer."""
        if self.consumer:
            try:
                self.consumer.close()
                self.logger.info("Kafka consumer closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing consumer: {str(e)}", exc_info=True) 