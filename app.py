"""
Stock Sentiment Analyzer - Main Application
"""
import streamlit as st
import os
from analyzer import StockSentimentAnalyzer
from news_fetcher import NewsFetcher
from reddit_fetcher import RedditFetcher

# Page config
st.set_page_config(
    page_title="Stock Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)

# Initialize
analyzer = StockSentimentAnalyzer()
news_fetcher = NewsFetcher()
reddit_fetcher = RedditFetcher()

# Header
st.title("📈 Stock Sentiment Analyzer")
st.markdown("AI-powered news sentiment analysis for stocks and crypto")

# Sidebar
with st.sidebar:
    st.header("Settings")
    num_articles = st.slider("Number of articles", 5, 20, 10)

    st.markdown("---")
    st.markdown("**Data Source:**")
    source = st.radio(
        "Fetch from",
        options=["News (NewsAPI)", "Reddit", "Both"],
        index=0,
        help=(
            "News: uses NewsAPI (set NEWS_API_KEY env var for live data).\n"
            "Reddit: scrapes r/wallstreetbets, r/stocks, r/investing, etc. — no key needed.\n"
            "Both: merges articles from both sources."
        ),
    )

    st.markdown("---")
    st.markdown("**API Status:**")
    if os.getenv("NEWS_API_KEY"):
        st.success("NewsAPI configured")
    else:
        st.warning("Set NEWS_API_KEY for live news")
    st.info("Reddit: no key needed ✓")

# Main input
col1, col2 = st.columns([2, 1])
with col1:
    ticker = st.text_input("Enter stock ticker", value="AAPL").upper().strip()
with col2:
    analyze_btn = st.button("Analyze", type="primary")

if analyze_btn and ticker:
    with st.spinner(f"Fetching and analyzing {'Reddit posts' if source == 'Reddit' else 'articles'} for {ticker}..."):
        try:
            articles = []

            if source in ("News (NewsAPI)", "Both"):
                news_articles = news_fetcher.get_news(ticker, num_articles)
                articles.extend(news_articles)

            if source in ("Reddit", "Both"):
                reddit_limit = num_articles if source == "Reddit" else num_articles // 2
                reddit_posts = reddit_fetcher.get_posts(ticker, num_posts=reddit_limit)
                articles.extend(reddit_posts)

            if not articles:
                st.error("No articles found. Try a different ticker.")
            else:
                # Analyze sentiment
                results = analyzer.analyze_articles(articles)

                if not results.get("articles"):
                    st.error("Analyzer returned no results.")
                else:
                    source_label = (
                        "Reddit posts" if source == "Reddit"
                        else "articles" if source == "News (NewsAPI)"
                        else "articles + posts"
                    )
                    st.success(f"Analyzed {len(results['articles'])} {source_label}")

                    # Score card
                    score = results['composite_score']
                    sentiment = results.get('overall_sentiment', 'N/A')

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Sentiment Score", f"{score:+d}", delta_color="normal")
                    with col2:
                        st.metric("Overall Sentiment", sentiment)
                    with col3:
                        st.metric("Positive", results['positive_count'])
                    with col4:
                        st.metric("Negative", results['negative_count'])

                    # Visualization
                    st.subheader("📊 Sentiment Distribution")
                    analyzer.plot_sentiment_distribution(results)

                    # Articles breakdown
                    st.subheader("📰 Article Analysis")
                    for i, article in enumerate(results['articles'], 1):
                        title_preview = article['title'][:65] + ("…" if len(article['title']) > 65 else "")
                        score_badge = "🟢" if article['sentiment'] == "Positive" else "🔴"
                        with st.expander(f"{score_badge} {i}. {title_preview}"):
                            st.write(f"**Source:** {article['source']}")
                            st.write(f"**Sentiment:** {article['sentiment']} ({article['score']:+d})")
                            if article.get('url'):
                                st.write(f"**Link:** [{article['url'][:60]}...]({article['url']})")
                            st.write(f"**Summary:** {article.get('description', 'N/A')[:200]}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Info section
st.markdown("---")
st.markdown("""
**Supported Tickers:** Any stock (AAPL, TSLA, GOOGL) or crypto (BTC, ETH)
**Reddit source** pulls from r/wallstreetbets, r/stocks, r/investing, r/StockMarket, r/options — no API key required.
""")
