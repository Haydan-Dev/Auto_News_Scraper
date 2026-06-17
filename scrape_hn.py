"""Scrape the latest headlines from Hacker News (https://news.ycombinator.com/).
Generates a dark-themed HTML page and opens it in the default browser.
"""

import webbrowser
from html import escape
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Hacker News front page URL
HN_URL = "https://news.ycombinator.com/"

# How many headlines to include on the page
TOP_N = 10

# Output file name (saved next to this script)
OUTPUT_FILE = Path(__file__).parent / "news_frontend.html"


def fetch_hn_page(url: str) -> str:
    """
    Fetch the Hacker News homepage over HTTPS.
    Returns the raw HTML as a string.
    """
    # Use a User-Agent so the server treats us like a normal browser
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; HN-Scraper/1.0)",
    }

    # timeout prevents the script from hanging if the site is slow or unreachable
    response = requests.get(url, headers=headers, timeout=10)

    # Raise an error for bad status codes (404, 500, etc.)
    response.raise_for_status()

    return response.text


def parse_headlines(html: str) -> list[tuple[str, str]]:
    """
    Parse story titles and URLs from the HTML.
    Returns a list of (title, url) tuples in page order.
    """
    soup = BeautifulSoup(html, "html.parser")

    headlines = []

    # Each story row on HN has class "athing"
    for story_row in soup.select("tr.athing"):
        # The title link lives inside span.titleline
        link = story_row.select_one("span.titleline > a")
        if link is None:
            continue

        title = link.get_text(strip=True)
        url = link.get("href", "")

        # Some links are relative (e.g. "item?id=123"); make them absolute
        if url.startswith("item?"):
            url = f"https://news.ycombinator.com/{url}"

        headlines.append((title, url))

    return headlines


def build_html_page(headlines: list[tuple[str, str]], count: int = TOP_N) -> str:
    """
    Build a complete HTML page string with a dark theme and clickable cards.
    """
    # Build each headline as a clickable card (escape text to keep HTML safe)
    cards_html = []
    for index, (title, url) in enumerate(headlines[:count], start=1):
        safe_title = escape(title)
        safe_url = escape(url, quote=True)
        cards_html.append(
            f"""
            <a class="card" href="{safe_url}" target="_blank" rel="noopener noreferrer">
                <span class="card-number">{index}</span>
                <span class="card-title">{safe_title}</span>
                <span class="card-arrow" aria-hidden="true">→</span>
            </a>"""
        )

    cards_block = "\n".join(cards_html)

    # Full page with embedded CSS for a modern dark theme
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hacker News — Top {count}</title>
    <style>
        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
            background: linear-gradient(160deg, #0f0f14 0%, #1a1a2e 50%, #16213e 100%);
            color: #e8e8f0;
            min-height: 100vh;
            padding: 2.5rem 1.5rem 3rem;
        }}

        .container {{
            max-width: 720px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 2.5rem;
        }}

        header h1 {{
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #ff6600, #ff9933);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        header p {{
            margin-top: 0.5rem;
            color: #8888a0;
            font-size: 0.95rem;
        }}

        .cards {{
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }}

        .card {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.1rem 1.25rem;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s ease, box-shadow 0.2s ease,
                        border-color 0.2s ease, background 0.2s ease;
        }}

        .card:hover {{
            transform: translateY(-3px);
            background: rgba(255, 102, 0, 0.08);
            border-color: rgba(255, 102, 0, 0.35);
            box-shadow: 0 8px 24px rgba(255, 102, 0, 0.15);
        }}

        .card-number {{
            flex-shrink: 0;
            width: 2rem;
            height: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 700;
            color: #ff6600;
            background: rgba(255, 102, 0, 0.12);
            border-radius: 8px;
        }}

        .card-title {{
            flex: 1;
            font-size: 1rem;
            line-height: 1.45;
            font-weight: 500;
        }}

        .card-arrow {{
            flex-shrink: 0;
            font-size: 1.1rem;
            color: #666680;
            transition: transform 0.2s ease, color 0.2s ease;
        }}

        .card:hover .card-arrow {{
            transform: translateX(4px);
            color: #ff9933;
        }}

        footer {{
            margin-top: 2.5rem;
            text-align: center;
            font-size: 0.8rem;
            color: #55556a;
        }}

        footer a {{
            color: #ff6600;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Hacker News</h1>
            <p>Top {count} headlines right now</p>
        </header>
        <div class="cards">
            {cards_block}
        </div>
        <footer>
            Scraped from <a href="https://news.ycombinator.com/" target="_blank" rel="noopener noreferrer">news.ycombinator.com</a>
        </footer>
    </div>
</body>
</html>"""


def save_html(html_content: str, filepath: Path) -> None:
    """Write the HTML string to a local file."""
    filepath.write_text(html_content, encoding="utf-8")


def open_in_browser(filepath: Path) -> None:
    """Open the saved HTML file in the system's default web browser."""
    # file:// URI works on Windows, macOS, and Linux
    webbrowser.open(filepath.resolve().as_uri())


def main() -> None:
    try:
        # Step 1: Download the page
        html = fetch_hn_page(HN_URL)

        # Step 2: Extract titles and links
        headlines = parse_headlines(html)

        if not headlines:
            print("No headlines found. The page layout may have changed.")
            return

        # Step 3: Build the HTML page from the top stories
        page_html = build_html_page(headlines, TOP_N)

        # Step 4: Save locally and open in the browser
        save_html(page_html, OUTPUT_FILE)
        open_in_browser(OUTPUT_FILE)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Hacker News. The website may be down.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again later.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: HTTP request failed ({err.response.status_code}).")
    except requests.exceptions.RequestException as err:
        print(f"Error: Failed to fetch the page — {err}")


if __name__ == "__main__":
    main()