"""
SQLAlchemy models for financial data storage.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockPrice(Base):
    """Model for storing stock price data."""
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StockPrice(symbol='{self.symbol}', timestamp='{self.timestamp}')>"

class StockAnalysis(Base):
    """Model for storing processed stock analysis data."""
    __tablename__ = 'stock_analysis'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False, index=True)
    window_start = Column(DateTime, nullable=False)
    window_end = Column(DateTime, nullable=False)
    avg_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    min_price = Column(Float, nullable=False)
    trade_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StockAnalysis(symbol='{self.symbol}', window_start='{self.window_start}')>" 