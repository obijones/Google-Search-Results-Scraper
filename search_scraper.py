import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import random
import os
from datetime import datetime

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0 Safari/537.36'
]

def random_sleep(min_time=2, max_time=5):
    """Sleep for a random amount of time"""
    time.sleep(random.uniform(min_time, max_time))

def setup_driver():
    """Set up and return a browser instance using undetected-chromedriver"""
    try:
        options = uc.ChromeOptions()
        
        user_agent = random.choice(USER_AGENTS)
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        
        driver = uc.Chrome(
            options=options,
            version_main=127
        )
        
        print(f"Using User-Agent: {user_agent}")
        return driver
        
    except Exception as e:
        print(f"Failed to initialize WebDriver: {str(e)}")
        raise

def read_search_query(filename="search_query.txt"):
    """Read the search query from a text file"""
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return None

def perform_search(driver, query):
    """Perform Google search with humanized behavior"""
    try:
        print("Navigating to Google...")
        driver.get("https://www.google.com/")
        random_sleep(3, 6)
        
        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print("Search box found")
        
        search_box.clear()
        random_sleep(0.5, 1.5)
        
        for char in query:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))
        
        random_sleep(0.5, 2)
        search_box.submit()
        print("Search submitted")
        
        # Wait for results and ads to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
        
        # Extra wait time for ads to load
        random_sleep(5, 8)
        
        # Try to find and print sponsored ads using multiple selectors
        try:
            ad_selectors = [
                "div[aria-label='Ads']",
                "#tads",
                "#tadsb",
                "div.commercial-unit-desktop-top",
                "div.ad_cclk",
                "div[data-text-ad='1']",
                "div.uEierd"  # Common class for ad containers
            ]
            
            found_ads = False
            print("\nSearching for ads using different selectors...")
            
            for selector in ad_selectors:
                ad_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if ad_elements:
                    print(f"\nFound ads using selector: {selector}")
                    print("-------------------")
                    for ad in ad_elements:
                        try:
                            # Get the entire text content of the ad
                            ad_text = ad.text
                            if ad_text:
                                print("Ad Content:")
                                print(ad_text)
                                print("-------------------")
                                found_ads = True
                        except Exception as e:
                            print(f"Error extracting ad content: {e}")
                            continue
            
            if not found_ads:
                print("No sponsored ads found with any selector")
                
        except Exception as e:
            print(f"Error extracting ads: {str(e)}")
        
        # Capture the page content
        page_content = driver.page_source
        if page_content:
            print(f"Captured {len(page_content)} bytes of content")
            return page_content
            
    except Exception as e:
        print(f"Error performing search: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        return None

def save_results(html_content, query):
    """Save the search results to an HTML file with timestamp"""
    if not html_content:
        print("No content to save")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if not os.path.exists('search_results'):
        os.makedirs('search_results')
    
    filename = f"search_results/search_results_{timestamp}.html"
    
    try:
        formatted_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="search-query" content="{query}">
    <meta name="search-timestamp" content="{timestamp}">
</head>
<body>
{html_content}
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(formatted_html)
            
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"Results saved to {filename} ({size} bytes)")
        else:
            print("Warning: File was not created")
            
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def main():
    driver = None
    try:
        while True:
            if driver:
                driver.quit()
                random_sleep(3, 7)
            
            driver = setup_driver()
            print("Browser initialized")
            
            query = read_search_query()
            if not query:
                print("No valid search query found. Waiting before retry...")
                random_sleep(45, 75)
                continue
            
            print(f"Performing search for: {query}")
            
            html_content = perform_search(driver, query)
            if html_content:
                save_results(html_content, query)
            
            delay = random.randint(60, 120)
            print(f"Waiting {delay} seconds before next search...")
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nScript terminated by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed")

if __name__ == "__main__":
    main()
