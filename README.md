# Auto News Scraper 📰

A fast, lightweight Python scraper that fetches the latest headlines from Hacker News and displays them in a beautiful dark-themed HTML page. One command to get the top stories in your browser!

## Features ✨

- **Live Scraping** - Fetches real-time headlines from Hacker News
- **Dark Theme UI** - Modern, responsive HTML interface with dark mode
- **Auto-Open Browser** - Automatically launches the page in your default browser
- **Clickable Cards** - Each headline is a clickable link to the full story
- **Error Handling** - Graceful handling of network issues and timeouts
- **Fast & Lightweight** - Minimal dependencies, quick execution

## Installation 📦

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

That's it! No API keys needed.

## Usage 🚀

Run the scraper:

```bash
python scrape_hn.py
```

The script will:
1. Fetch the latest Hacker News homepage
2. Extract the top 10 headlines
3. Generate a beautiful HTML page
4. Automatically open it in your browser

## What You Get 🎨

A clean HTML page with:
- **Top 10 Headlines** - The most recent stories from Hacker News
- **Clickable Links** - Click any headline to read the full story
- **Dark Theme** - Easy on the eyes with a modern dark mode design
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Visual Feedback** - Hover effects and smooth animations

## Example Output

The script generates `news_frontend.html` with:
- A gradient dark background
- Numbered headline cards
- Hover animations and transitions
- Direct links to each story on Hacker News
- Professional typography and spacing

## Requirements 📋

See `requirements.txt`:
- `requests` - HTTP library for fetching web pages
- `beautifulsoup4` - HTML parsing and scraping

## Configuration ⚙️

You can customize the scraper by editing these variables in `scrape_hn.py`:

```python
HN_URL = "https://news.ycombinator.com/"  # Hacker News URL
TOP_N = 10                                  # Number of headlines to show
OUTPUT_FILE = Path(__file__).parent / "news_frontend.html"  # Output file location
```

## How It Works 🔧

1. **Fetch Page** - Downloads the Hacker News homepage with proper headers
2. **Parse HTML** - Uses BeautifulSoup to extract story titles and links
3. **Generate Page** - Builds a complete HTML page with embedded CSS styling
4. **Save & Open** - Saves the file and opens it in your default browser

## Error Handling 🛡️

The script gracefully handles:
- Network connection failures
- Request timeouts (10 second default)
- HTTP errors (404, 500, etc.)
- Missing or changed page layout

## Performance ⚡

- **Execution Time**: Usually 1-3 seconds (depending on internet speed)
- **File Size**: ~15-25 KB HTML output
- **No Server Needed**: Completely local, runs on your machine

## Customization 🎨

Want to customize the HTML theme? Edit the CSS in `build_html_page()` function:
- Change colors, fonts, spacing, and animations
- Add additional styling for dark/light mode toggle
- Modify the layout and card design

## Troubleshooting 🛠️

**"Could not connect to Hacker News"?**
- Check your internet connection
- Hacker News may be temporarily down
- Try again in a few moments

**"No headlines found"?**
- The page layout may have changed
- The scraping selectors might need updating
- Try visiting https://news.ycombinator.com/ directly

**HTML file not opening?**
- Check that the output file was created
- Ensure your default browser is set correctly
- Try opening `news_frontend.html` manually

## Output Files 📁

- `news_frontend.html` - Generated HTML page with the top headlines

## License 📄

Open source - feel free to modify and use as needed

## Contributing 🤝

Found a bug or want to add features? Feel free to fork and submit improvements!

## Inspiration

Built to make Hacker News browsing faster and more beautiful. Perfect for quick daily reading!