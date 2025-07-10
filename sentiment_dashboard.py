import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Supabase project info
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@st.cache_data(ttl=300)
def load_data():
    res = (
        supabase
        .table("comments")
        .select("*")
        .order("published_at", desc=True)
        .limit(1000)
        .execute()
    )
    df = pd.DataFrame(res.data)
    # Convert published_at to datetime.date
    df['published_at'] = pd.to_datetime(df['published_at']).dt.date
    return df

# Load data once
df = load_data()

st.title("📊 YouTube Comments Sentiment Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date range filter
min_date, max_date = df['published_at'].min(), df['published_at'].max()
date_range = st.sidebar.date_input(
    "Date range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Sentiment filter
sentiment_choices = ['positive', 'neutral', 'negative']
selected_sentiments = st.sidebar.multiselect(
    "Sentiment",
    ['all'] + sentiment_choices,
    default=['all']
)

# Author filter (top 20)
top_authors = df['author'].value_counts().index.tolist()[:20]
selected_authors = st.sidebar.multiselect(
    "Authors (top 20)",
    ['all'] + top_authors,
    default=['all']
)

# Keyword search
keyword = st.sidebar.text_input("Keyword search in comment text")

# Apply filters
filtered = df.copy()
filtered = filtered[
    (filtered['published_at'] >= date_range[0]) &
    (filtered['published_at'] <= date_range[1])
]
if 'all' not in selected_sentiments:
    filtered = filtered[filtered['sentiment'].isin(selected_sentiments)]
if 'all' not in selected_authors:
    filtered = filtered[filtered['author'].isin(selected_authors)]
if keyword:
    filtered = filtered[
        filtered['text_clean'].str.contains(keyword, case=False, na=False)
    ]

st.sidebar.markdown(f"**Total comments:** {len(filtered)}")

# 1. Overall Sentiment Distribution
st.header("1. Overall Sentiment Distribution")
sent_counts = filtered['sentiment'].value_counts().reset_index()
sent_counts.columns = ['sentiment', 'count']
fig1 = px.pie(
    sent_counts,
    values='count',
    names='sentiment',
    title="Sentiment Breakdown"
)
st.plotly_chart(fig1, use_container_width=True)

# 2. Daily Sentiment Trend
st.header("2. Daily Sentiment Trend")
trend = (
    filtered
    .groupby(['published_at', 'sentiment'])
    .size()
    .reset_index(name='count')
)
fig2 = px.line(
    trend,
    x='published_at',
    y='count',
    color='sentiment',
    title="Daily Count by Sentiment",
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Top Commenting Authors
st.header("3. Top Commenting Authors")
author_counts = (
    filtered['author']
    .value_counts()            # absolute counts
    .reset_index(name='count')
)
author_counts.columns = ['author', 'count']
author_counts['count'] = author_counts['count'].astype(int)
top10 = author_counts.head(10)
fig3 = px.bar(
    top10,
    x='count',
    y='author',
    orientation='h',
    title="Top 10 Authors by Comment Volume",
    labels={'count': 'Number of Comments', 'author': 'Author'}
)
st.plotly_chart(fig3, use_container_width=True)

# 4. Sentiment Score Distribution
st.header("4. Sentiment Score Distribution")
fig4 = px.histogram(
    filtered,
    x='sentiment_score',
    nbins=30,
    title="Histogram of Sentiment Scores"
)
st.plotly_chart(fig4, use_container_width=True)

# 5. Recent Comments Table
st.header("5. Recent Comments Table")
n_rows = st.slider(
    "Number of recent comments to display",
    min_value=5,
    max_value=50,
    value=20
)
table_df = (
    filtered
    .sort_values('published_at', ascending=False)
    .head(n_rows)[
        ['published_at', 'author', 'text_clean', 'sentiment', 'sentiment_score']
    ]
)
styled = (
    table_df
    .style
    .highlight_max(subset=['sentiment_score'], color='lightgreen')
    .highlight_min(subset=['sentiment_score'], color='lightcoral')
)
st.dataframe(styled, use_container_width=True)
