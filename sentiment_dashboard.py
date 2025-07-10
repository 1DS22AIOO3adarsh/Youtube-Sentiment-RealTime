import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

<<<<<<< HEAD
load_dotenv()
=======
conn = psycopg2.connect(
    host="db.auxvvnieyzkijcjfaosg.supabase.co",
    port=6543,
    database="postgres",
    user="postgres",
    password="cvU8Sdk8eUh86zJR"
)
>>>>>>> fd20daa69266378ff341d115dc1811e181fe682b

# Your Supabase project info
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

@st.cache_data(ttl=300)
def load_data():
    # Fetch data from 'comments' table
    data = supabase.table("comments").select("*").order("published_at", desc=True).limit(100).execute()
    df = pd.DataFrame(data.data)
    return df

st.title("YouTube Comments Sentiment Dashboard")

df = load_data()

if st.checkbox("Show raw data"):
    st.write(df)

# Sentiment distribution
sentiment_counts = df['sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['sentiment', 'count']

fig = px.pie(sentiment_counts, values='count', names='sentiment', title='Sentiment Distribution')
st.plotly_chart(fig)

# Recent comments
st.subheader("Recent Comments with Sentiment")
for _, row in df.iterrows():
    st.write(f"**{row['author']}**: {row['text_clean']} ({row['sentiment']}, score: {row['sentiment_score']:.2f})")
