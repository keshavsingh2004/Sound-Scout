from st_pages import Page, add_page_title, show_pages
from pathlib import Path
## Declaring the pages in your app:
show_pages(
    [
        Page("pages/home.py", "Home"),
        Page("pages/top_5.py", "Top 5"),
        Page("pages/comparison.py", "Comparison"),
        Page("pages/analysisofgenre.py","Analysis of Genre"),
        Page("pages/linear","LinearRegression")
    ]
)
add_page_title()
