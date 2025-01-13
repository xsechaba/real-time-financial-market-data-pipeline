"""
Script to run the real-time streaming pipeline.
"""
import time
import signal
import threading
from datetime import datetime
from ingestion.alpha_vantage_client import AlphaVantageClient
from ingestion.kafka_producer import StockDataProducer
from processing.kafka_consumer import StockDataConsumer
from utils.logging_config import setup_logger
from utils.validation import validate_stock_data, validate_symbol

# Set up logging
logger = setup_logger('streaming_pipeline')

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    global running
    logger.info("Shutdown signal received. Cleaning up...")
    running = False

def run_producer(symbols):
    """Run the Kafka producer to fetch and publish stock data."""
    client = AlphaVantageClient()
    producer = StockDataProducer()
    
    try:
        while running:
            for symbol in symbols:
                try:
                    if not validate_symbol(symbol):
                        logger.error(f"Invalid symbol format: {symbol}")
                        continue
                        
                    logger.info(f"Fetching data for {symbol}...")
                    data = client.get_stock_data(symbol)
                    
                    # Check for API error messages
                    if "Error Message" in data:
                        logger.error(f"API Error for {symbol}: {data['Error Message']}")
                        continue
                    
                    if "Note" in data:
                        logger.warning(f"API Note: {data['Note']}")
                        # If we hit rate limit, wait longer
                        if "API call frequency" in data["Note"]:
                            logger.warning("Rate limit hit, waiting 60 seconds...")
                            time.sleep(60)
                            continue
                    
                    # Get the latest data point
                    time_series = data.get("Time Series (1min)", {})
                    if time_series:
                        latest_time = list(time_series.keys())[0]
                        latest_data = time_series[latest_time]
                        
                        # Format data for Kafka
                        stock_data = {
                            'timestamp': latest_time,
                            'open_price': latest_data['1. open'],
                            'high_price': latest_data['2. high'],
                            'low_price': latest_data['3. low'],
                            'close_price': latest_data['4. close'],
                            'volume': latest_data['5. volume']
                        }
                        
                        # Validate data before publishing
                        validation_error = validate_stock_data(stock_data)
                        if validation_error:
                            logger.error(f"Data validation failed for {symbol}: {validation_error}")
                            continue
                        
                        # Publish to Kafka
                        producer.publish_stock_data(symbol, stock_data)
                        logger.info(f"Successfully published {symbol} data")
                    else:
                        logger.warning(f"No time series data available for {symbol}")
                    
                except Exception as e:
                    logger.error(f"Error processing {symbol}: {str(e)}", exc_info=True)
                
                # Sleep longer between requests to respect API limits
                time.sleep(20)  # Increased from 15 to 20 seconds
            
            # Add a small delay between cycles
            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
    finally:
        producer.close()

def run_consumer():
    """Run the Kafka consumer to process streaming data."""
    while running:
        try:
            consumer = StockDataConsumer()
            consumer.process_messages()
        except Exception as e:
            logger.error(f"Consumer error: {str(e)}", exc_info=True)
            logger.info("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
        finally:
            try:
                consumer.close()
            except:
                pass

def main():
    """Main function to run the streaming pipeline."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    symbols = ['IBM', 'AAPL', 'MSFT']
    logger.info(f"Starting streaming pipeline for symbols: {', '.join(symbols)}")
    
    # Start consumer in a separate thread
    consumer_thread = threading.Thread(target=run_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()
    
    # Run producer in main thread
    run_producer(symbols)
    
    # Wait for consumer thread to finish
    global running
    running = False
    consumer_thread.join(timeout=5)
    logger.info("Streaming pipeline shutdown complete")

if __name__ == "__main__":
    main() 