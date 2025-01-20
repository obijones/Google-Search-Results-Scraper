# Google Search Results Scraper

A Python script that performs automated Google searches and saves the results (including sponsored ads) in HTML format. The script uses undetected-chromedriver to avoid detection and implements human-like behavior patterns.

## Features

- Automated Google searches with human-like behavior
- Captures both organic and sponsored results
- Saves results in formatted HTML files
- Rotating user agents
- Configurable search intervals
- Headless browser operation
- Anti-detection measures

## Prerequisites

- Python 3.x
- Google Chrome Browser (version 127)
- Linux/Unix environment (tested on Kali Linux)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/google-search-scraper.git
cd google-search-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Chrome version 127:
```bash
# Remove current Chrome version if exists
sudo apt remove google-chrome-stable

# Download Chrome version 127
wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_127.0.6533.119-1_amd64.deb

# Install Chrome
sudo dpkg -i google-chrome-stable_127.0.6533.119-1_amd64.deb
sudo apt --fix-broken install

# Prevent automatic updates
sudo apt-mark hold google-chrome-stable
```

## Usage
1. Create a search query file:
```bash
echo "your search query" > search_query.txt
```

2. Run the script:
```bash
python3 search_scraper.py
```
The script will:
- Initialize a headless Chrome browser
- Read the search query from search_query.txt
- Perform the search on Google
- Save results in HTML format in the 'search_results' directory
- Wait for a random interval (60-120 seconds) before the next search
- Continue until interrupted with Ctrl+C

## File Structure
![image](https://github.com/user-attachments/assets/407cee6f-86c9-4f56-8633-74ca7c8fef80)


## Configuration
You can modify the following parameters in the script:

USER_AGENTS: List of user agents to rotate between
Search intervals in the random.randint(60, 120) call
Wait times in the random_sleep() function

## Output
The script creates HTML files in the 'search_results' directory with the following naming convention:
```bash
search_results_YYYYMMDD_HHMMSS.html
```
Each file contains:

Search metadata (query and timestamp)
Complete search results including sponsored ads
Original HTML structure and formatting

Error Handling
The script includes comprehensive error handling for:

WebDriver initialization failures
Network issues
Google detection/blocking
File system operations

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This script is for educational purposes only. Be aware that automated scraping of Google search results may violate Google's terms of service. Use responsibly and at your own risk.

## Known Issues
May require periodic updates to maintain effectiveness against detection
Chrome version must match ChromeDriver version (127.x)
Some anti-bot measures may still detect the automation
