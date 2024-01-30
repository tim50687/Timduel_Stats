#!/bin/bash

# Step 1: Install required packages
pip3 install -r requirements.txt

# Step 2: Navigate to the 'spider' directory
cd nba_game_time/nba_game_time

# Step 3: Remove the 'today_match.json' file if it exists
rm -f today_match.json

# Step 4: Run Scrapy to crawl NBA match data in the background and capture the PID (Process ID) of the background process
scrapy crawl match_scraper & scrapy_pid=$!

# Step 5: Wait for the Scrapy process to finish
wait $scrapy_pid

# Step 6: Run the Google Calendar integration script
python3 google_calendar_integration.py && cd ../..

# Step 7: Print a "done" message
echo "Done! Check your Google Calendar for the NBA match schedule."
