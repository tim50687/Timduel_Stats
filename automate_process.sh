#!/bin/bash

# Step 1: Navigate to the 'spider' directory
cd nba_game_time/nba_game_time

# Step 2: Remove the 'today_match.json' file if it exists
rm -f today_match.json

# Step 3: Run Scrapy to crawl NBA match data in the background and capture the PID (Process ID) of the background process
scrapy crawl match_scraper & scrapy_pid=$!

# Step 4: Wait for the Scrapy process to finish
wait $scrapy_pid

# Step 5: Run the Google Calendar integration script
python3 google_calendar_integration.py && cd ../..

# Step 6: Print a "done" message
echo "Done! Check your Google Calendar for the NBA match schedule."
