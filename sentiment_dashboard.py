import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from collections import Counter

conn = psycopg2.connect(
    host="db.auxvvnieyzkijcjfaosg.supabase.co",
    port=6543,
    database="postgres",
    user="postgres",
    password="cvU8Sdk8eUh86zJR"
)


# Fetch data
@st.cache_data(ttl=300)
def load_data():
    query = """
        SELECT comment_id, author, text_clean, sentiment, sentiment_score, published_at
        FROM comments
        ORDER BY published_at DESC
        LIMIT 500
    """
    df = pd.read_sql(query, conn)
    return df

st.title("YouTube Comments Sentiment Dashboard")

df = load_data()

# Convert published_at to datetime
df['published_at'] = pd.to_datetime(df['published_at'])
df['date'] = df['published_at'].dt.date

# Sentiment filter
sentiment_options = ['all', 'positive', 'negative', 'neutral']
selected_sentiment = st.selectbox("Filter comments by sentiment", sentiment_options)

if selected_sentiment != 'all':
    df = df[df['sentiment'] == selected_sentiment]

# Show raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Sentiment distribution
sentiment_counts = df['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

fig_pie = px.pie(sentiment_counts, values='count', names='sentiment', title='Sentiment Distribution')
st.plotly_chart(fig_pie)

# Sentiment trend over time
st.subheader("Sentiment Trend Over Time")
trend_df = df.groupby(['date', 'sentiment']).size().reset_index(name='count')

fig_trend = px.line(
    trend_df,
    x='date',
    y='count',
    color='sentiment',
    markers=True,
    title='Sentiment count over time'
)
st.plotly_chart(fig_trend)

# Most frequent words
st.subheader("Top 10 Most Frequent Words")
all_words = ' '.join(df['text_clean'].tolist()).split()
common_words = Counter(all_words).most_common(10)
common_df = pd.DataFrame(common_words, columns=['word', 'count'])

fig_words = px.bar(common_df, x='word', y='count', title='Most Common Words')
st.plotly_chart(fig_words)

# Author-level summary
st.subheader("Top Commenting Authors")
author_df = df.groupby('author').size().reset_index(name='comment_count')
author_df = author_df.sort_values(by='comment_count', ascending=False).head(10)

fig_authors = px.bar(author_df, x='author', y='comment_count', title='Authors with Most Comments')
st.plotly_chart(fig_authors)

# Show recent comments
st.subheader("Recent Comments with Sentiment")
for _, row in df.iterrows():
    st.write(f"**{row['author']}**: {row['text_clean']} ({row['sentiment']}, score: {row['sentiment_score']:.2f})")

conn.close()
