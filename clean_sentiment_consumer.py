from kafka import KafkaConsumer, KafkaProducer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import re

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'raw_comments',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def clean_text(text):
    text = re.sub(r"http\S+", "", text)      # Remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)  # Remove special chars
    text = text.lower().strip()
    return text

print("Consumer started. Listening to raw_comments...")

for message in consumer:
    comment = message.value
    raw_text = comment['text']
    cleaned_text = clean_text(raw_text)
    sentiment_scores = sia.polarity_scores(cleaned_text)

    # Assign a label
    if sentiment_scores['compound'] >= 0.05:
        sentiment = "positive"
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Add results to comment
    comment['text_clean'] = cleaned_text
    comment['sentiment'] = sentiment
    comment['sentiment_score'] = sentiment_scores['compound']

    # Send to processed_comments topic
    producer.send('processed_comments', value=comment)
    print(f"Processed and sent comment ID: {comment['comment_id']} — Sentiment: {sentiment}")

producer.flush()
