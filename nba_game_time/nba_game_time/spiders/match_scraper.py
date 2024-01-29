import scrapy
import json
from datetime import date
from nba_game_time.items import MatchItem


class MatchScraperSpider(scrapy.Spider):
    name = "match_scraper"
    start_urls = ["https://www.nba.com/schedule"]

    headers = {
        ':authority': 'cdn.nba.com',
        ':method': 'GET',
        ':path': '/static/json/staticData/scheduleLeagueV2_1.json',
        ':scheme': 'https',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/',
        'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }

    def parse(self, response):
        url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"

        yield scrapy.Request(
            url=url, callback=self.parse_schedule, headers=self.headers)

    def parse_schedule(self, response):
        match = MatchItem()
        # Get today date
        date_string = date.today().strftime("%m/%d/%Y") + " 00:00:00"

        # Get 2023 - 2024 match schedule
        raw_data = response.body
        data = json.loads(raw_data)
        schedules = data["leagueSchedule"]["gameDates"]

        # Get today match
        for schedule in schedules:
            if schedule["gameDate"] == date_string:
                today_match = schedule["games"]
                for each_match in today_match:
                    match['game_id'] = each_match["gameId"]
                    match['game_date_time_est'] = each_match["gameDateTimeEst"]
                    match['game_date_time_utc'] = each_match["gameDateTimeUTC"]
                    match['arena_city'] = each_match["arenaCity"]
                    match['arena_state'] = each_match["arenaState"]
                    match['arena_name'] = each_match["arenaName"]
                    match['home_team'] = each_match["homeTeam"]["teamCity"] + \
                        " " + each_match["homeTeam"]["teamName"]
                    match['away_team'] = each_match["awayTeam"]["teamCity"] + \
                        " " + each_match["awayTeam"]["teamName"]
                    yield match
