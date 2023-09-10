import requests
from bs4 import BeautifulSoup
import pandas as pd

from config import BASE_URL
from utils import safe_get_text

class ContractScraper:
    """
    A class used to scrape contract data from contractsfinder.service.gov.uk
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
    
    def fetch_content(self, url):
        """Fetch the page content using a requests session."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve content: {e}")
            return None

    def parse_content(self, content):
        """Parse the content using BeautifulSoup."""
        return BeautifulSoup(content, 'html.parser')

    def extract_data(self, soup):
        """Extract required data from the soup object."""
        all_data = soup.find_all("div", {"class": "search-result"})
        
        csv_file = [
            {
                "Tender": safe_get_text(item, "a", "govuk-link search-result-rwh break-word"),
                "Company": safe_get_text(item, "div", "search-result-sub-header wrap-test"),
                "Procurement": safe_get_text(item, "div", "search-result-entry", index=0).replace("Procurement stage", ""),
                "Notice": safe_get_text(item, "div", "search-result-entry", index=1).replace("Notice status",""),
                "Location": safe_get_text(item, "div", "search-result-entry", index=3).replace("Contract location", ""),
                "Closing": safe_get_text(item, "div", "search-result-entry", index=2).replace("Closing", ""),
                "Value": safe_get_text(item, "div", "search-result-entry", index=4).replace("Contract value", ""),
                "Date": safe_get_text(item, "div", "search-result-entry", index=5).replace("Publication date", ""),
            }
            for item in all_data
        ]
        return csv_file

    def save_to_csv(self, data):
        """Save the extracted data to a CSV file."""
        df = pd.DataFrame(data)
        df.to_csv("Scraper.csv", index=False)

    def run(self):
        """Run the scraper for a range of pages and compile the results."""
        csv_file = []
        for page in range(1, 125):
            url = f"{BASE_URL}{page}#dashboard_notices.html"
            content = self.fetch_content(url)
            if content:
                soup = self.parse_content(content)
                csv_file.extend(self.extract_data(soup))
        self.save_to_csv(csv_file)
