import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from src.core.logger import get_logger

logger = get_logger("search_agent")

# -----------------------------
# Search Agent
# -----------------------------
def search_google_news(query, max_results=5):
    """
    Search Google News RSS feed for a given query and return up to `max_results` results.
    Returns a list of dicts with title, url, and source.
    """
    encoded_query = quote_plus(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}"

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")[:max_results]

        results = []
        for item in items:
            title = item.title.text
            link = item.link.text
            source = item.source.text if item.source else "Google News"
            results.append({"title": title, "url": link, "source": source})

        logger.info(f"Found {len(results)} articles for query: '{query}'")
        return results

    except requests.RequestException as e:
        logger.error(f"Failed to fetch Google News RSS for '{query}': {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error during news search: {e}")
        return []
