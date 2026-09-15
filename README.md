# PTI Live News Fetcher

A professional Streamlit web application that fetches live news from the PTI API and acts as a multi-source news aggregator using public RSS feeds as a fallback mechanism.

## Features
- **Original API Integration:** Connects to the paid PTI API using a custom centercode.
- **Bulletproof Fallback:** Automatically scrapes Google News and other RSS feeds if the main API goes down or the subscription expires.
- **Smart Date Filtering:** Strict 24-hour rolling window for today's date, and 00:00 to 23:59 for past dates.
- **UI Pagination:** Breaks down large volumes of news into clean 10-article pages for easy reading.

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit application from the root directory:
```bash
python -m streamlit run src/main.py
```
