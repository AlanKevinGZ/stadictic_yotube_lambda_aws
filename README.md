# YouTube Channel Analytics ETL Pipeline on AWS

## Overview

This project implements an automated **ETL (Extract, Transform, Load) pipeline** on AWS to collect statistics from multiple YouTube channels using the **YouTube Data API v3**.

The solution automatically extracts channel metrics, stores historical snapshots in Amazon S3, catalogs the data with AWS Glue, enables SQL analytics through Amazon Athena, and sends email notifications whenever a new dataset is generated.

---

## Architecture

```text
                EventBridge Scheduler
                        │
                        ▼
              AWS Lambda (ETL)
                        │
        Extract YouTube Data API v3
                        │
                        ▼
                 Amazon S3 (raw/)
                        │
            S3 Event Notification
               ┌────────┴────────┐
               ▼                 ▼
      AWS Glue Crawler     Lambda Notification
               │                 │
               ▼                 ▼
        Glue Data Catalog     Amazon SNS
               │                 │
               ▼                 ▼
          Amazon Athena      Email Notification
```

---

# Technologies

- Python 3.13
- AWS Lambda
- Amazon S3
- Amazon EventBridge Scheduler
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- Amazon SNS
- YouTube Data API v3
- Pandas
- Boto3

---

# Project Structure

```text
.
├── lambda_etl/
│   └── lambda_function.py
│
├── lambda_notification/
│   └── lambda_function.py
│
├── channels.json
│
└── README.md
```

---

# ETL Workflow

## 1. Extract

The ETL Lambda is executed manually or automatically by **Amazon EventBridge Scheduler**.

The function:

- Reads a list of YouTube Channel IDs from Amazon S3.
- Calls the YouTube Data API.
- Retrieves:
  - Channel Name
  - Total Views
  - Subscribers
  - Video Count
- Creates a Pandas DataFrame.

---

## 2. Transform

The extracted data is transformed into a structured tabular format.

Each execution stores a historical snapshot with a timestamp.

Example:

| Channel | Subscribers | Views | Created_at |
|----------|------------:|------:|------------|
| PlayStation | 17,200,000 | 6,303,512,374 | 2026-07-30 22:21:16 |

The timestamp allows historical comparisons over time.

---

## 3. Load

The resulting CSV is uploaded automatically to Amazon S3.

Example:

```text
raw/youtube_stats_2026-07-30_22-21-16.csv
```

---

# AWS Services

## AWS Lambda (ETL)

Responsible for:

- Reading channel IDs
- Calling the YouTube API
- Transforming the data
- Uploading CSV snapshots to Amazon S3

---

## Amazon S3

Stores:

- Channel configuration (`channels.json`)
- Historical CSV snapshots

Example:

```text
raw/
    youtube_stats_2026-07-30_22-21-16.csv
    youtube_stats_2026-07-30_23-00-05.csv
    youtube_stats_2026-07-31_09-00-00.csv
```

---

## Amazon EventBridge Scheduler

Automatically executes the ETL Lambda every day.

Example schedule:

```text
09:00 UTC
```

This enables fully automated data collection.

---

## AWS Glue Crawler

Automatically scans the S3 bucket and creates metadata inside the Glue Data Catalog.

---

## AWS Glue Data Catalog

Creates the table used later by Amazon Athena.

Example schema:

| Column | Type |
|---------|------|
| channel_id | string |
| created_at | string |
| channel_name | string |
| total_views | bigint |
| subscribers | bigint |
| video_count | bigint |

---

## Amazon Athena

Allows querying the historical data using standard SQL.

Examples include:

- Historical snapshots
- Subscriber growth
- View growth
- Window Functions
- Analytical SQL

---

## Amazon SNS

When a new CSV file is uploaded to Amazon S3:

1. S3 detects the new object.
2. S3 triggers a notification Lambda.
3. The Lambda publishes a message to Amazon SNS.
4. SNS sends an email notification automatically.

Example email:

```text
Subject:

YouTube ETL Pipeline - SUCCESS

Body:

Pipeline executed successfully.

Bucket:
demo-output-youtube-lamda

File:
raw/youtube_stats_2026-07-30_22-21-16.csv

Status:
SUCCESS
```

---

# SQL Analytics

Example query to calculate view growth using a Window Function.

```sql
WITH stats AS (

SELECT
    channel_name,
    total_views,

    LAG(total_views) OVER(
        PARTITION BY channel_name
        ORDER BY created_at
    ) previous_views,

    created_at

FROM raw

)

SELECT

channel_name,
created_at,
total_views,
previous_views,
total_views-previous_views AS new_views

FROM stats;
```

---

# Features

- Automated ETL pipeline
- Historical snapshots
- Event-driven architecture
- Daily scheduling
- Serverless implementation
- SQL analytics
- Email notifications
- Scalable AWS architecture

---

# Learning Outcomes

During this project the following AWS services and concepts were implemented:

- AWS Lambda
- Amazon S3
- Amazon SNS
- EventBridge Scheduler
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- Event Notifications
- YouTube Data API
- Pandas
- Boto3
- ETL Pipelines
- Serverless Architecture
- Event-Driven Processing
- Analytical SQL
- Window Functions
- Historical Data Snapshots

---

# Author

**Alan Kevin Gonzalez Hernandez**
