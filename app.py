from st_pages import Page, add_page_title, show_pages
from pathlib import Path
## Declaring the pages in your app:
show_pages(
    [
        Page("home.py", "Home", "🏠"),
        Page("top_5.py", "Top 5", "🏆"),
        Page("comparison.py", "Comparison", "⚖️"),
    ]
)

add_page_title()
