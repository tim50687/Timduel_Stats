import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone, timedelta
import pytz


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
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None
        
    @staticmethod
    def parse_data(data):
        """
        Parses the data from the Fangraphs website.

        Args:
            data (str): The text content of the response.

        Returns:
            dict: The parsed data.
        """
        return data
    
    @staticmethod
    def save_data(data, file_path="data/fangraphs_data.json"):
        """
        Saves the data to a JSON file.

        Args:
            data (dict): The data to save.
            file_path (str): The path to the JSON file.
        """
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_data(file_path="data/fangraphs_data.json"):
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
    def get_or_fetch_data(urls, file_path="data/fangraphs_data.json"):
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
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path), tz=est)
            file_date = file_mtime.date()
            today_date = now_est.date()

            if file_date == today_date:
                return FangraphsScraper.load_data(file_path)
        
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
    urls = "https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&team=0&pageitems=2000000000&qual=5&sortcol=9&sortdir=default&type=24&month=1000&startdate=2024-07-02&enddate=2024-07-06"
    data = FangraphsScraper.fetch_data(urls)
    print(data)
