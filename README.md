# Timduel Stats

**Timduel Stats** is a Flask-based front-end application that integrates sports data, starting with Major League Baseball (MLB). It provides real-time game schedules, player stats, home run odds, and home run predictions. The application fetches data from various sources and displays the information through an easy-to-use web interface.

## Features
- **Sports Data Integration:** Currently focused on MLB, with plans to add more sports in the future.
- **User-Friendly Interface:** Displays real-time stats, predictions, and odds in a clean and accessible format.

## MLB Features

### MLB Game Schedule
- Displays daily MLB game schedules, fetched from Amazon S3.

### Home Run Odds
- Shows home run odds for specific games, sorted and processed by bookmakers.

### Player Stats
- Displays detailed player statistics for selected teams, including fly-ball and hard-hit data.

### Home Run Prediction
- Provides predictions for whether a player will hit a home run based on statistical models.

## Future Plans
- **More Sports:** Plans to expand the app to include other sports such as NBA, NFL, and more.
- **Additional Features:** Add more detailed statistical analysis, predictions, and odds tracking for other sports.

### Available Routes

- **/schedule** - Displays the MLB game schedule.
- **/odds** - Shows the home run odds for a selected game.
- **/player_stats** - Displays player stats for two selected teams.
- **/hr_prediction** - Shows home run predictions for players.

### Image Attribution

- **Images**: The images used in this application are sourced from Pinterest. The original images can be found at:
  - [Kyrie Irving](https://www.pinterest.com/pin/39054721765075714/)
  - [Tom Brady](https://www.pinterest.com/pin/54535845471401635/)
  - [Shohei Ohtani](https://www.pinterest.com/pin/86272149105009925/)
