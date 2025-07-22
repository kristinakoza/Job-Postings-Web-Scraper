from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime, timezone
import time
import random
import sys
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_chrome_driver():
    options = Options()
    
    # Essential options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    
    # Realistic user agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    
    # Remove automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    return webdriver.Chrome(service=Service(), options=options)

def fetch_html(url):
    driver = None
    try:
        driver = get_chrome_driver()
        driver.get(url)
        
        # Wait for jobs to load or Cloudflare to pass
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.job, div.job"))
        )
        
        # Additional random delay
        time.sleep(random.uniform(2, 5))
        
        html_content = driver.page_source
        
        # Save for debugging
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Saved page HTML to debug.html")
        
        return html_content
        
    except Exception as e:
        print(f"Error fetching page: {str(e)}", file=sys.stderr)
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {str(e)}", file=sys.stderr)

def parse_jobs(html_content):
    if not html_content:
        return []
        
    soup = BeautifulSoup(html_content, "html.parser")
    jobs = []
    
    for job in soup.select("tr.job, div.job"):
        try:
            title = job.select_one("h2")
            company = job.select_one("h3")
            link_tag = job.select_one("a.preventLink")

            if title and company and link_tag:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True),
                    "link": f"https://remoteok.com{link_tag.get('href')}",
                    "scraped_at": datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            print(f"Error parsing job: {str(e)}")
            continue
    
    print(f"Found {len(jobs)} jobs")
    return jobs

def save_to_google_sheets(jobs, sheet_name="job_postings"):
    if not jobs:
        print("No jobs to save")
        return
        
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(sheet_name).sheet1
        sheet.clear()
        sheet.append_row(["Title", "Company", "Link", "Scraped At"])
        
        for job in jobs:
            sheet.append_row([
                job["title"],
                job["company"],
                job["link"],
                job["scraped_at"]
            ])
        
        print(f"Saved {len(jobs)} jobs to Google Sheets")
    except Exception as e:
        print(f"Google Sheets error: {str(e)}")

def filter_jobs(jobs, keyword):
    return [j for j in jobs if keyword.lower() in j["title"].lower()]
def save_to_csv(jobs, filepath="data/remoteok_jobs.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pd.DataFrame(jobs).to_csv(filepath, index=False)
    print(f"Saved {len(jobs)} jobs to {filepath}")

def main():
    url = "https://remoteok.com/remote-sales-marketing-jobs"
    
    print("Starting scrape...")
    html_content = fetch_html(url)
    
    if not html_content:
        print("Failed to fetch page content", file=sys.stderr)
        return
        
    jobs = parse_jobs(html_content)
    
    if jobs:
        save_to_csv(jobs)
        save_to_google_sheets(jobs)
    else:
        print("No jobs found - check debug_page.html to see what was fetched")

if __name__ == "__main__":
    main()