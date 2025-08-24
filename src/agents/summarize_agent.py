import os
import requests
from bs4 import BeautifulSoup
from readability import Document
from playwright.sync_api import sync_playwright
from openai import OpenAI
from dotenv import load_dotenv
from src.core.logger import get_logger

# Load .env for API keys, etc.
load_dotenv()

client = OpenAI()
logger = get_logger("summarize_agent")

# -----------------------------
# Article Text Extraction
# -----------------------------
def extract_text(url_raw, timeout=15000):
    """
    Extract article title and content from a given URL using Playwright and Readability.
    Returns a tuple (title, text).
    """
    try:
        # Resolve redirection (Google RSS URLs)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_raw, headers=headers, timeout=10, allow_redirects=True)
        url = response.url
    except Exception as e:
        logger.warning(f"Failed to resolve redirect for {url_raw}: {e}")
        url = url_raw  # fallback to original URL

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0"
            )
            page = context.new_page()
            page.goto(url, timeout=timeout)

            try:
                # Attempt to dismiss cookie banners
                page.click('button:has-text("Accept all")', timeout=3000)
            except:
                pass

            html = page.content()
            browser.close()

        doc = Document(html)
        title = doc.title() or "Untitled"
        summary_html = doc.summary()
        text = BeautifulSoup(summary_html, "html.parser").get_text().strip()

        if not text:
            logger.warning(f"No readable content found at {url}")
            return title, "[No readable content found]"

        logger.info(f"Extracted article from {url}")
        return title, text[:6000]  # Truncate to avoid long payloads

    except Exception as e:
        logger.error(f"Error extracting article from {url}: {e}")
        return "Untitled", f"[Extraction error: {e}]"

# -----------------------------
# Article Summarization
# -----------------------------
def summarize(text, model="gpt-4o", temperature=0.4):
    """
    Summarize article text using OpenAI GPT model.
    """
    try:
        # noinspection PyTypeChecker
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes regulatory news for climate experts."},
                {"role": "user", "content": f"Summarize the following article:\n\n{text}"}
            ],
            temperature=temperature
        )
        summary = response.choices[0].message.content
        logger.info("Summary generated successfully")
        return summary
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return f"[Summary error: {e}]"
