from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz
import os
# Selenium imports
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class FangraphsScraper:
    @staticmethod
    def fetch_data(url):
        """
        Fetches data from the specified URL.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            str: The text content of the response.
        """
        # Use Selenium to fetch the data
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        driver.get(url)
        # Wait for the page to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fg-data-grid.table-type"))
        )

        html_content = driver.page_source
        driver.quit()
        return html_content
        
    @staticmethod
    def parse_data(html_content):
        """
        Parses the data from the Fangraphs website.

        Args:
            data (str): The text content of the response.

        Returns:
            dict: The parsed data.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the table div by its class
        table_div = soup.find('div', {'class': 'fg-data-grid table-type'})
        rows = table_div.find('table').find_all('tr', class_=True)
        print(rows)
        data = []
        for row in rows:
            columns = row.find_all('td')
            row_data = {
                'name': columns[1].text.strip(),
                'FB+': columns[18].text.strip()
            }
            data.append(row_data)
        return data

    
    @staticmethod
    def save_data(data, file_path="../../../data/fangraphs_data.json"):
        """
        Saves the data to a JSON file.

        Args:
            data (dict): The data to save.
            file_path (str): The path to the JSON file.
        """
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_data(file_path="../../../data/fangraphs_data.json"):
        """
        Loads the data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The loaded data.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return None
        
    @staticmethod
    def get_or_fetch_data(urls, file_path="../../../data/fangraphs_data.json"):
        """
        Get the data from a JSON file if it exists and is not outdated,
        otherwise fetch it from the URLs and save it to the file.

        Args:
            urls (list): List of URLs to fetch data from.
            file_path (str): The path to the data JSON file.

        Returns:
            dict: The data.
        """
        est = pytz.timezone('US/Eastern')
        now_est = datetime.now(est)

        # Check if the file exists and is not outdated
        # if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        #     file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=est)
        #     file_date = file_mtime.date()
        #     today_date = now_est.date()

        #     if file_date == today_date:
        #         return FangraphsScraper.load_data(file_path)
        
        # Fetch the data
        data = {}
        for url in urls:
            html_content = FangraphsScraper.fetch_data(url)
            if html_content:
                parsed_data = FangraphsScraper.parse_data(html_content)
                # Process and store the parsed data
                data[url] = str(parsed_data)  # Placeholder for actual data processing
        FangraphsScraper.save_data(data)
        
        return data
    

if __name__ == "__main__":
    urls = ["https://www.fangraphs.com/leaders/major-league/robot.txt?pageitems=2000000000&startdate=2024-07-02&enddate=2024-07-06&season=2024&season1=2024&month=1000&ind=0&team=0&type=23"]
    data = FangraphsScraper.get_or_fetch_data(urls)
    # print(data)


