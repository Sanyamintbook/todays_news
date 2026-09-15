import requests
from datetime import datetime
import json
import feedparser

def fetch_live_pti(date_str=None, source="All"):
    """Fetch live news from various sources for a given date (DD-MM-YYYY). Defaults to today."""
    if not date_str:
        date_str = datetime.now().strftime('%d-%m-%Y')
        
    try:
        day, month, year = date_str.split('-')
        from_time = f"{year}/{month}/{day} 00:00:00"
        end_time = f"{year}/{month}/{day} 23:59:59"
        
        resource_host = 'http://editorial.pti.in/ptiapi/webservice1.asmx/JsonFile1'
        centercode = f"{day}{month}{year}001MNT"
        
        params = {
            'centercode': centercode,
            'FromTime': from_time,
            'EndTime': end_time
        }
        
        if source == "All" or source == "PTI":
            response = requests.get(resource_host, params=params, timeout=5)
            # Check if response is valid JSON and not empty
            if response.status_code == 200 and response.text.strip():
                try:
                    pti_json = response.json()
                    if pti_json: # If it's a valid, non-empty JSON response
                        return pti_json
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
        
    # FETCH FROM PUBLIC RSS FEEDS (Fallback and Multi-source)
    try:
        from email.utils import parsedate_to_datetime
        from datetime import timezone, timedelta
        import urllib.parse 
        
        # Check if the requested date is today's date
        is_today = date_str == datetime.now().strftime('%d-%m-%Y')
        
        feeds_to_fetch = []
        
        # 1. Google News Search (For PTI)
        if source == "All" or source == "PTI":
            if is_today:
                search_query = "PTI news India when:2d"
            else:
                target_date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                import datetime as dt
                prev_ymd = (target_date_obj - dt.timedelta(days=1)).strftime('%Y-%m-%d')
                next_ymd = (target_date_obj + dt.timedelta(days=2)).strftime('%Y-%m-%d')
                search_query = f"PTI news India after:{prev_ymd} before:{next_ymd}"
                
            encoded_query = urllib.parse.quote(search_query)
            feeds_to_fetch.append(("PTI", f'https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en'))
            
        # 2. Other Public RSS Feeds
        OTHER_FEEDS = {
            "Times of India": "http://timesofindia.indiatimes.com/rssfeedstopstories.cms",
            "Hindustan Times": "https://www.hindustantimes.com/feeds/topnews/rssfeed.xml",
            "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
            "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss"
        }
        
        for name, url in OTHER_FEEDS.items():
            if source == "All" or source == name:
                feeds_to_fetch.append((name, url))
                
        news_list = []
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        
        # Fetch from all selected feeds
        for feed_name, feed_url in feeds_to_fetch:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    try:
                        # Parse the UTC published date and convert to IST
                        if hasattr(entry, 'published'):
                            dt_utc = parsedate_to_datetime(entry.published)
                        else:
                            continue # Skip if no date
                            
                        dt_ist = dt_utc.astimezone(ist_tz)
                        
                        # STRICT FILTERING
                        include_article = False
                        if is_today:
                            now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
                            twenty_four_hours_ago = now_ist - timedelta(hours=24)
                            if twenty_four_hours_ago <= dt_ist <= now_ist:
                                include_article = True
                        else:
                            if dt_ist.strftime('%d-%m-%Y') == date_str:
                                include_article = True
                                
                        if include_article:
                            news_list.append({
                                "source": feed_name,
                                "title": entry.title,
                                "link": entry.link,
                                "published": dt_ist.strftime('%Y-%m-%d %H:%M:%S %p'),
                                "dt_obj": dt_ist # keep object for sorting
                            })
                    except Exception:
                        pass
            except Exception:
                pass
                
        # Sort combined list by date descending (latest first)
        news_list.sort(key=lambda x: x["dt_obj"], reverse=True)
        
        # Remove the raw datetime object before returning
        for item in news_list:
            del item["dt_obj"]
            
        if news_list:
            return news_list
        return []
    except Exception as e:
        return {"error": f"Failed to fetch news: {str(e)}"}
