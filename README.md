# Real-Time Financial Market Data Pipeline

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%E2%9C%93-blue.svg)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7.1-green.svg)](https://airflow.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust, scalable data pipeline for real-time collection, processing, and analysis of financial market data from Alpha Vantage API. Built with modern data engineering practices and containerized for easy deployment.

<p align="center">
  <img src="docs/images/pipeline_architecture.png" alt="Pipeline Architecture" width="800"/>
</p>

## 🚀 Features

- **Real-time Data Collection**: Automated fetching of stock market data from Alpha Vantage API
- **Robust Data Storage**: PostgreSQL database for reliable data persistence
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
│   └── db_operations.py       # Database handling
└── utils/            # Shared utilities
    └── logging_config.py      # Logging setup

airflow/              # Airflow configuration
├── dags/
│   └── market_data_pipeline.py # Pipeline DAG
└── logs/             # Airflow logs
```

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