from kafka import KafkaConsumer
import json
import psycopg2

# Kafka consumer
consumer = KafkaConsumer(
    'processed_comments',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="youtube_sentiment",
    user="postgres",
    password="1234"
)
cursor = conn.cursor()

insert_query = """
    INSERT INTO comments (comment_id, video_id, author, text_clean, sentiment, sentiment_score, published_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (comment_id) DO NOTHING;
"""

print("DB consumer started. Listening to processed_comments...")

for message in consumer:
    comment = message.value

    cursor.execute(
        insert_query,
        (
            comment['comment_id'],
            comment['video_id'],
            comment['author'],
            comment['text_clean'],
            comment['sentiment'],
            comment['sentiment_score'],
            comment['published_at']
        )
    )
    conn.commit()
    print(f"Inserted comment ID: {comment['comment_id']}")

# Close connection when done
cursor.close()
conn.close()
