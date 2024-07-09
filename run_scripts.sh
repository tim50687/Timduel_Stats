#!/bin/bash

# Remove all data files end with json
echo "Removing all data files..."
rm -f ./data/*.json

# Run the first Python script
echo "Running the first Python script..."
python3 ./app/mlb/mlb_schedule/web_scraping/fangraphs_scraper.py

# Run the second Python script
echo "Running the second Python script..."
python3 ./run.py

echo "All scripts executed."
