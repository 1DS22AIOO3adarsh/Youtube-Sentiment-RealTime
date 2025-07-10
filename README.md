Absolutely — let’s update the README to include **Google Cloud Console usage** (if you used it to manage or deploy services, for example, Kafka or VM-based hosting), and add your live Streamlit app link at the end.

Here’s the **final, polished README** (full copy-ready):

---

# YouTube Real-Time Sentiment Analysis Pipeline

## Overview

This project implements a **real-time sentiment analysis system** for YouTube comments. It scrapes new comments, analyzes their sentiment, stores them in a PostgreSQL database (hosted on Supabase), and visualizes the results through a live Streamlit dashboard.

The system was built as an end-to-end data engineering and data science pipeline to demonstrate real-time data streaming, processing, and visualization.

---

## Features

* **Real-time data ingestion** using a Kafka producer to scrape YouTube comments.
* **Streaming processing** using a Kafka consumer that cleans text and analyzes sentiment.
* **Centralized storage** in Supabase PostgreSQL.
* **Interactive dashboard** using Streamlit, deployed and publicly accessible.
* Sentiment breakdown (positive, negative, neutral) with score distributions.
* Recent comments view with author and score details.

---

## Architecture

```
YouTube Scraper (Producer)
     ↓
Apache Kafka Topic
     ↓
Kafka Consumer (Preprocessing + Sentiment Analysis)
     ↓
Supabase PostgreSQL
     ↓
Streamlit Dashboard (Live Visualization)
```

---

## Tech Stack

* Python
* Apache Kafka (Confluent Platform)
* Supabase PostgreSQL
* Streamlit
* Docker (for local orchestration)
* Plotly (for charts)
* psycopg2 (PostgreSQL connector)
* NLP: VADER sentiment analysis (lexicon-based)
* Google Cloud Console (for managing VMs and resources)

---

## Setup Instructions

### Prerequisites

* Docker (for Kafka and local setup)
* Python 3.10+
* Supabase account (for managed PostgreSQL)
* Google Cloud Console account (optional for hosting VMs or Kafka services)
* Streamlit Cloud (for dashboard deployment)

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Youtube-Sentiment-RealTime.git
cd Youtube-Sentiment-RealTime
```

---

### 2. Configure Supabase

* Create a Supabase project.
* Get your database connection URL and service role key.
* Create a table `comments` with columns:

  * `comment_id`
  * `video_id`
  * `author`
  * `text_clean`
  * `sentiment`
  * `sentiment_score`
  * `published_at`
  * `fetched_at`

---

### 3. Update connection info

In your consumer and Streamlit code, update:

```python
conn = psycopg2.connect(
    host="db.YOUR-SUPABASE-HOST.supabase.co",
    port=5432,
    database="postgres",
    user="postgres",
    password="YOUR-SUPABASE-PASSWORD"
)
```

---

### 4. Run Kafka stack

```bash
docker-compose up -d
```

---

### 5. Run producer and consumer

```bash
python producer/producer.py
python consumer/consumer.py
```

---

### 6. Deploy Streamlit dashboard

* Push your repo to GitHub.
* Connect to Streamlit Cloud, set your `SUPABASE_URL` and `SUPABASE_PASSWORD` as secrets.
* Deploy.

---

## How to use

* Start the producer to collect new YouTube comments.
* The consumer processes them and writes to Supabase.
* The dashboard automatically reads from Supabase and displays live data.
* Use refresh or built-in auto-refresh button to get the latest insights.

---


## Challenges and how we tackled them

### Kafka connection issues

We faced initial configuration issues with Kafka and Zookeeper networking. We resolved this by defining clear advertised listeners and using Docker Compose (or GCP VMs) for consistent orchestration.

---

### PostgreSQL remote access

While deploying, we encountered errors like "connection refused" due to Supabase connection from Streamlit Cloud. We solved this by using correct Supabase connection strings and securely configuring credentials via Streamlit secrets.

---

### Permission errors when exporting data

We initially tried using `COPY TO` from PostgreSQL, which caused local file permission errors. We fixed this by switching to `\copy` in `psql`, which performs client-side exports.

---

### Git conflicts and push issues

We faced remote branch conflicts while pushing updated code. We resolved it by running `git pull --rebase` before pushing again to keep local and remote histories aligned.

---

### Streamlit auto-refresh

Streamlit does not auto-refresh by default. We added manual refresh buttons and optional interval-based auto-refresh to ensure dashboard data stayed current without restarting services.

---

## Future improvements

* Switch from VADER to a transformer-based sentiment model (e.g., DistilBERT).
* Add author-level analytics, word clouds, or topic modeling.
* Use Airflow or GCP Workflows for full orchestration and scheduling.
* Add Slack or email notifications on sentiment spikes.

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue first to discuss your ideas.

---

## License

This project is licensed under the MIT License.

---

## Live Demo

Check out the live Streamlit dashboard here:
**[YouTube Sentiment Realtime Dashboard](https://youtube-sentiment-realtime-em3x63btnlrovliiwskq8x.streamlit.app)**

---

