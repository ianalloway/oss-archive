"""
Stock Sentiment Analyzer - Main Application
"""
import streamlit as st
import os
from analyzer import StockSentimentAnalyzer
from news_fetcher import NewsFetcher

# Page config
st.set_page_config(
    page_title="Stock Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

# Initialize
analyzer = StockSentimentAnalyzer()
news_fetcher = NewsFetcher()

# Header
st.title("📈 Stock Sentiment Analyzer")
st.markdown("AI-powered news sentiment analysis for stocks and crypto")

# Sidebar
with st.sidebar:
    st.header("Settings")
    num_articles = st.slider("Number of articles", 5, 20, 10)
    
    st.markdown("---")
    st.markdown("**API Status:**")
    if os.getenv("NEWS_API_KEY"):
        st.success("NewsAPI configured")
    else:
        st.warning("Set NEWS_API_KEY")

# Main input
col1, col2 = st.columns([2, 1])
with col1:
    ticker = st.text_input("Enter stock ticker", value="AAPL").upper().strip()
with col2:
    analyze_btn = st.button("Analyze", type="primary")

if analyze_btn and ticker:
    with st.spinner(f"Fetching and analyzing news for {ticker}..."):
        try:
            # Fetch news
            articles = news_fetcher.get_news(ticker, num_articles)
            
            if not articles:
                st.error("No articles found. Try a different ticker.")
            else:
                # Analyze sentiment
                results = analyzer.analyze_articles(articles)
                
                # Display results
                st.success(f"Analyzed {len(articles)} articles")
                
                # Score card
                score = results['composite_score']
                sentiment = results['overall_sentiment']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sentiment Score", f"{score:+d}", delta_color="normal")
                with col2:
                    st.metric("Sentiment", sentiment)
                with col3:
                    st.metric("Articles Analyzed", len(articles))
                
                # Visualization
                st.subheader("📊 Sentiment Distribution")
                analyzer.plot_sentiment_distribution(results)
                
                # Articles breakdown
                st.subheader("📰 Article Analysis")
                for i, article in enumerate(results['articles'], 1):
                    with st.expander(f"{i}. {article['title'][:60]}..."):
                        st.write(f"**Source:** {article['source']}")
                        st.write(f"**Sentiment:** {article['sentiment']} ({article['score']:+d})")
                        st.write(f"**Summary:** {article.get('description', 'N/A')[:200]}")
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Info section
st.markdown("---")
st.markdown("""
**Supported Tickers:** Any stock (AAPL, TSLA, GOOGL) or crypto (BTC, ETH)
""")
