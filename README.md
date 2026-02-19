# Stock Sentiment Analyzer

AI/ML app that analyzes news sentiment for stocks and crypto.

**Live Demo**: Coming soon

## Features

- **Real-time News Fetch**: Gets latest news for any stock ticker
- **Sentiment Analysis**: Uses NLP to determine positive/negative/neutral sentiment
- **Visualization**: Interactive charts showing sentiment over time
- **Score Calculation**: Composite sentiment score (-100 to +100)
- **Keyword Extraction**: Identifies key themes and topics

## Tech Stack

- **Python** - Core language
- **Streamlit** - Web UI
- **Transformers** - Hugging Face sentiment model
- **NewsAPI** - News data (free tier)
- **Plotly** - Interactive visualizations

## Quick Start

```bash
# Clone and setup
git clone https://github.com/ianalloway/stock-sentiment-analyzer.git
cd stock-sentiment-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Usage

1. Enter a stock ticker (e.g., AAPL, TSLA, BTC)
2. Select number of articles to analyze
3. View sentiment analysis results
4. See composite score and visualizations

## Project Structure

```
stock-sentiment-analyzer/
├── app.py              # Streamlit UI
├── analyzer.py         # Sentiment analysis logic
├── news_fetcher.py     # News API integration
├── requirements.txt    # Dependencies
└── README.md
```

## API Keys Required

- **NewsAPI**: Get free key at https://newsapi.org

Set as environment variable:
```bash
export NEWS_API_KEY=your_key_here
```

## Example Output

| Ticker | Score | Sentiment | Articles |
|--------|-------|-----------|----------|
| AAPL   | +45   | Positive  | 10       |
| TSLA   | -12   | Neutral   | 10       |
| BTC    | +28   | Positive  | 10       |

## License

MIT - Ian Alloway
