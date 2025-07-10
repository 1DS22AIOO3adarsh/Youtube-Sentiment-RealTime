from kafka import KafkaProducer
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()



# Your YouTube API key
API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = os.getenv("VIDEO_ID") 
# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_comments(video_id, max_comments=50):
    comments = []
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    ).execute()

    while response and len(comments) < max_comments:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'comment_id': item['id'],
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'published_at': comment['publishedAt'],
                'video_id': video_id
            })
            if len(comments) >= max_comments:
                break

        if 'nextPageToken' in response and len(comments) < max_comments:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            ).execute()
        else:
            break

    return comments

if __name__ == "__main__":
    comments = fetch_comments(VIDEO_ID, max_comments=50)

    for comment in comments:
        # Send each comment to Kafka
        producer.send('raw_comments', value=comment)

    producer.flush()
    print(f"Sent {len(comments)} comments to Kafka topic 'raw_comments'.")
