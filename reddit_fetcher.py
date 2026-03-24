"""
Stock Sentiment Analyzer - Reddit Fetcher Module

Pulls posts from finance-related subreddits using Reddit's public JSON API.
No API key or OAuth required — uses the anonymous read-only JSON endpoint.
"""
import time
from datetime import datetime, timezone
from typing import Optional
import requests

# Subreddits most relevant to stock/crypto discussion
FINANCE_SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "StockMarket",
    "options",
]

# Reddit's public JSON endpoint — no auth needed for read access
_REDDIT_SEARCH_URL = "https://www.reddit.com/r/{sub}/search.json"
_REDDIT_HEADERS = {
    "User-Agent": "stock-sentiment-analyzer/1.0 (educational project)"
}


class RedditFetcher:
    """Fetch Reddit posts mentioning a ticker from finance subreddits."""

    def __init__(self, subreddits: Optional[list[str]] = None):
        self.subreddits = subreddits or FINANCE_SUBREDDITS

    def get_posts(self, ticker: str, num_posts: int = 10) -> list[dict]:
        """
        Return a list of Reddit post dicts shaped like NewsAPI articles so they
        can be dropped straight into StockSentimentAnalyzer.analyze_articles().

        Fields returned per post:
          title, description, source, url, publishedAt
        """
        collected: list[dict] = []
        per_sub = max(1, num_posts // len(self.subreddits) + 1)

        for sub in self.subreddits:
            if len(collected) >= num_posts:
                break
            posts = self._fetch_subreddit(sub, ticker, per_sub)
            collected.extend(posts)
            # Be polite — Reddit rate-limits aggressive scrapers
            time.sleep(0.3)

        # De-duplicate by URL and trim to requested count
        seen: set[str] = set()
        unique: list[dict] = []
        for post in collected:
            if post["url"] not in seen:
                seen.add(post["url"])
                unique.append(post)
            if len(unique) >= num_posts:
                break

        return unique

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fetch_subreddit(
        self, subreddit: str, ticker: str, limit: int
    ) -> list[dict]:
        """Search a single subreddit for ticker mentions."""
        params = {
            "q": ticker,
            "sort": "new",
            "restrict_sr": "on",
            "limit": min(limit, 25),  # Reddit max per request is 100; 25 is safe
            "t": "month",  # posts from the last month
        }
        try:
            resp = requests.get(
                _REDDIT_SEARCH_URL.format(sub=subreddit),
                params=params,
                headers=_REDDIT_HEADERS,
                timeout=10,
            )
            if resp.status_code == 429:
                print(f"Reddit rate-limited on r/{subreddit}. Backing off.")
                time.sleep(2)
                return []
            if resp.status_code != 200:
                print(f"Reddit API error on r/{subreddit}: {resp.status_code}")
                return []

            children = resp.json().get("data", {}).get("children", [])
            return [self._shape_post(c["data"], subreddit) for c in children]

        except requests.exceptions.Timeout:
            print(f"Timeout fetching r/{subreddit}")
            return []
        except Exception as exc:
            print(f"Error fetching r/{subreddit}: {exc}")
            return []

    @staticmethod
    def _shape_post(post: dict, subreddit: str) -> dict:
        """Normalize a Reddit post dict to the NewsAPI article shape."""
        # Combine selftext (body) and title for richer sentiment analysis
        body = (post.get("selftext") or "").strip()
        # Reddit stores UTC timestamps as float epoch seconds
        created_utc = post.get("created_utc", 0)
        published = datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat()

        return {
            "title": post.get("title", ""),
            "description": body if body and body != "[removed]" else post.get("title", ""),
            "source": f"r/{subreddit}",
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "publishedAt": published,
            # Extra Reddit-specific metadata (ignored by analyzer, useful for display)
            "_score": post.get("score", 0),
            "_num_comments": post.get("num_comments", 0),
            "_author": post.get("author", ""),
        }
