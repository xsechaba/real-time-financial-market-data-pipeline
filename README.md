# Real-Time Financial Market Data Pipeline

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%E2%9C%93-blue.svg)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7.1-green.svg)](https://airflow.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust, scalable data pipeline for real-time collection, processing, and analysis of financial market data from Alpha Vantage API. Built with modern data engineering practices and containerized for easy deployment.

<p align="center">
  <img src="docs/images/pipeline_architecture.png" alt="Pipeline Architecture" width="800"/>
</p>

## 📋 Table of Contents
- [Features](#-features)
- [Architecture](#️-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Data Flow](#-data-flow)
- [Configuration](#️-configuration)
- [Monitoring](#-monitoring)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🚀 Features

- **Real-time Data Collection**: Automated fetching of stock market data from Alpha Vantage API
- **Direct Database Integration**: Immediate PostgreSQL storage for reliable data persistence
- **Efficient Processing**: Pandas-based data analysis with 5-minute window aggregations
- **Automated Orchestration**: Apache Airflow DAGs for reliable pipeline scheduling
- **Containerized Setup**: Docker-based deployment for consistency across environments
- **Monitoring & Logging**: Comprehensive logging and pipeline monitoring
- **Error Handling**: Robust error handling and automatic retries
- **Scalable Architecture**: Designed for easy scaling and maintenance

## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

```
src/
├── ingestion/          # Data ingestion components
│   ├── data_ingestion.py      # Main ingestion logic
│   └── alpha_vantage_client.py # API client
├── processing/         # Data processing logic
│   ├── data_processor.py      # Data transformation
│   └── test_processor.py      # Unit tests
├── storage/           # Database operations
│   ├── database.py           # Database connection handling
│   ├── models.py            # Database models
│   └── init_db.py          # Database initialization
└── utils/            # Shared utilities
    ├── logging_config.py    # Logging configuration
    └── validation.py       # Data validation utilities

airflow/              # Airflow configuration
├── dags/
│   └── market_data_pipeline.py # Pipeline DAG
└── logs/             # Airflow logs
```

The pipeline consists of three main components:
1. **Data Collection**: Python scripts fetch data from Alpha Vantage API
2. **Data Storage**: Direct PostgreSQL integration for storing raw and processed data
3. **Data Processing**: Pandas-based analysis for calculating metrics and aggregations

All components are orchestrated by Apache Airflow, ensuring reliable scheduling and monitoring.

## 🔧 Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Alpha Vantage API key (free tier available)
- 4GB+ RAM recommended
- Internet connection for API access

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/xsechaba/real-time-financial-market-data-pipeline.git
cd real-time-financial-market-data-pipeline
```

2. **Set up Python environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configurations
```

5. **Start services:**
```bash
docker-compose up -d
```

## 🚀 Usage

1. **Access Airflow UI:**
   - Navigate to http://localhost:8081
   - Login with:
     - Username: `airflow`
     - Password: `airflow`

2. **Start the Pipeline:**
   - Enable the DAG 'market_data_pipeline'
   - Trigger manually or wait for scheduled execution
   - DAG runs every 30 minutes by default

3. **Monitor Operations:**
   - View task status in Airflow UI
   - Check logs in `airflow/logs/`
   - Query results in PostgreSQL

## 📊 Data Flow

1. **Data Collection** 📥
   - Real-time stock data from Alpha Vantage
   - Supported symbols: AAPL, MSFT, IBM
   - 5-minute interval data points
   - Automatic rate limiting
   - Handles API throttling and retries

2. **Data Storage** 💾
   - Raw data table: `stock_prices`
     ```sql
     - timestamp: TIMESTAMP
     - symbol: VARCHAR
     - open_price: DECIMAL
     - high_price: DECIMAL
     - low_price: DECIMAL
     - close_price: DECIMAL
     - volume: INTEGER
     ```
   - Processed data table: `stock_analysis`
     ```sql
     - window_start: TIMESTAMP
     - window_end: TIMESTAMP
     - symbol: VARCHAR
     - avg_price: DECIMAL
     - volume: INTEGER
     - num_trades: INTEGER
     ```

3. **Data Processing** ⚙️
   - 5-minute window aggregations
   - Volume-weighted average price (VWAP)
   - Moving averages calculation
   - Data validation and cleaning
   - Automatic error handling

## ⚙️ Configuration

Configure the pipeline through `.env` file:

```ini
# API Configuration
ALPHA_VANTAGE_API_KEY=your_api_key
API_CALL_INTERVAL=60

# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=financial_data
DB_USER=postgres
DB_PASSWORD=your_password

# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_PORT=8081
```

## 📈 Monitoring

1. **Airflow Monitoring:**
   - Task success/failure rates
   - Task duration metrics
   - DAG run history
   - Real-time task status

2. **Database Monitoring:**
   - Data ingestion rates
   - Storage utilization
   - Query performance
   - Connection pool status

3. **Application Logs:**
   - Detailed logging for all components
   - Error tracking and alerting
   - Performance metrics
   - Data quality checks

## 🔧 Troubleshooting

Common issues and solutions:

1. **Database Connection Issues:**
   - Verify PostgreSQL service is running
   - Check database credentials in `.env`
   - Ensure proper network connectivity

2. **API Rate Limiting:**
   - Monitor Alpha Vantage API usage
   - Adjust `API_CALL_INTERVAL` if needed
   - Check API key validity

3. **Airflow Task Failures:**
   - Check task logs in Airflow UI
   - Verify environment variables
   - Monitor resource utilization

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing the financial data API
- [Apache Airflow](https://airflow.apache.org/) for workflow orchestration
- [Docker](https://www.docker.com/) for containerization
- [PostgreSQL](https://www.postgresql.org/) for data storage
- [Pandas](https://pandas.pydata.org/) for data processing

## 📧 Contact

Sechaba Mohlabeng

Project Link: [https://github.com/xsechaba/real-time-financial-market-data-pipeline](https://github.com/xsechaba/real-time-financial-market-data-pipeline)