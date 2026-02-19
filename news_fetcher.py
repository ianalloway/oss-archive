"""
Stock Sentiment Analyzer - News Fetcher Module
"""
import os
import requests
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        
    def get_news(self, ticker, num_articles=10):
        """Fetch news articles for a given ticker"""
        if not self.api_key:
            # Return mock data if no API key
            return self._get_mock_data(ticker, num_articles)
        
        # Search for ticker news
        params = {
            'q': ticker,
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': num_articles
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('articles', [])
            else:
                print(f"API Error: {response.status_code}")
                return self._get_mock_data(ticker, num_articles)
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            return self._get_mock_data(ticker, num_articles)
    
    def _get_mock_data(self, ticker, num_articles):
        """Generate mock data when API is not available"""
        mock_articles = [
            {
                'title': f"{ticker} Reports Strong Q4 Earnings, Beats Expectations",
                'description': f"{ticker} exceeded analyst expectations with strong quarterly results, driven by increased demand and operational efficiency.",
                'source': {'name': 'Financial Times'},
                'url': 'https://example.com',
                'publishedAt': datetime.now().isoformat()
            },
            {
                'title': f"Analysts Upgrade {ticker} to Buy Rating",
                'description': f"Multiple Wall Street analysts have upgraded {ticker} to buy, citing positive growth outlook and market position.",
                'source': {'name': 'Bloomberg'},
                'url': 'https://example.com',
                'publishedAt': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                'title': f"{ticker} Announces New Product Launch",
                'description': f"{ticker} unveiled its latest product line, which investors see as a potential growth catalyst.",
                'source': {'name': 'Reuters'},
                'url': 'https://example.com',
                'publishedAt': (datetime.now() - timedelta(hours=5)).isoformat()
            },
            {
                'title': f"Market Watch: {ticker} Faces Headwinds",
                'description': f"Despite recent gains, {ticker} faces challenges from increased competition and regulatory scrutiny.",
                'source': {'name': 'CNBC'},
                'url': 'https://example.com',
                'publishedAt': (datetime.now() - timedelta(hours=8)).isoformat()
            },
            {
                'title': f"{ticker} CEO Discusses Future Strategy",
                'description': f"In a recent interview, the CEO outlined plans for expansion and innovation at {ticker}.",
                'source': {'name': 'WSJ'},
                'url': 'https://example.com',
                'publishedAt': (datetime.now() - timedelta(days=1)).isoformat()
            }
        ]
        return mock_articles[:num_articles]
