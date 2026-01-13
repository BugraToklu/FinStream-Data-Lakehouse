# FinStream: Real-time Financial Data Lakehouse

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-Latest-black)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-orange)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-Storage-blue)
![Trino](https://img.shields.io/badge/Trino-Query%20Engine-pink)
![dbt](https://img.shields.io/badge/dbt-Transformation-orange)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-green)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)

FinStream is an end-to-end data engineering project designed to ingest, process, store, and analyze financial trade data in real-time.

This project simulates a scalable **Data Lakehouse** environment, implementing the modern **Medallion Architecture** (Bronze, Silver, Gold layers) to ensure data quality and accessibility. It integrates industry-standard tools for streaming, ACID transactions, and orchestration.

## Architecture

The pipeline consists of the following stages:

1.  **Ingestion:** A Python-based API simulator generates synthetic trade data and pushes it to **Apache Kafka**.
2.  **Streaming:** **Apache Spark Structured Streaming** consumes data from Kafka and writes it to **MinIO (S3)** in **Delta Lake** format.
3.  **Storage (Bronze Layer):** Raw data is stored with ACID transaction guarantees.
4.  **Transformation (Silver & Gold Layers):** **dbt (data build tool)** cleans raw data and aggregates it into business-ready reporting tables.
5.  **Serving:** **Trino** serves as the distributed SQL query engine, allowing high-performance analytics on the Data Lake.
6.  **Orchestration:** **Apache Airflow** schedules and manages the transformation workflows.

```mermaid
graph LR
    subgraph "Ingestion Layer"
    A[Python Trade API] -->|JSON| B(Apache Kafka)
    end

    subgraph "Streaming Layer"
    B -->|Stream| C{Apache Spark}
    C -->|Write Delta| D[(MinIO S3 / Bronze)]
    end

    subgraph "Storage Layer"
    D -.->|Read| E[Trino Query Engine]
    end

    subgraph "Transformation Layer (dbt)"
    E -->|Transform| F[(Silver: Cleaned)]
    F -->|Agg| G[(Gold: Market Summary)]
    end

    subgraph "Orchestration"
    H[Apache Airflow] -->|Trigger| F
    H -->|Trigger| G
    end

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#dfd,stroke:#333,stroke-width:2px