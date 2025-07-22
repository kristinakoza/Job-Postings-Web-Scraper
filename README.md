# Job-Postings-Web-Scraper
A robust web scraper that extracts remote sales and marketing job listings from RemoteOK, designed to showcase clean Python implementation and web scraping skills.

A robust web scraper that extracts remote sales and marketing job listings from RemoteOK, designed to showcase clean Python implementation and web scraping skills.

Features
Cloudflare Bypass: Uses Selenium with anti-detection configurations
Structured Data Extraction: Parses job titles, companies, and links
CSV Export: Saves results to organized CSV files
Debugging Tools: Auto-saves raw HTML for troubleshooting
Error Handling: Comprehensive exception management
Google Sheets: Saves all the data to Google Sheets (requires some extra files that I didn't upload due to privacy reasons_. 

Tech Stack
Python 3.8+
Selenium WebDriver (with Chrome)
BeautifulSoup4 for HTML parsing
Pandas for data export
webdriver-manager for automatic driver setup

When running, it creates two files (oone of them requires to have a "data" folder)
data/remoteok_jobs.csv (structured job data)
debug_page.html (raw HTML for debugging)


remoteok-scraper/
├── scraper.py            # Main scraping script
├── requirements.txt      # Dependencies
├── data/                 # Output directory for CSVs
├── README.md             # This file
└── .gitignore            # Standard Python gitignore

Why This Project?
This implementation demonstrates:
Real-world web scraping with anti-bot evasion
Clean, modular Python code following best practices
Error handling for production reliability
Data processing with Pandas
Debugging practices with HTML snapshots
Save to Google Sheets so it would be available anywhere to anyone who has the link
