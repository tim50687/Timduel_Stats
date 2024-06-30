# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NbaGameTimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MatchItem(scrapy.Item):
    # team info
    game_date_time_est = scrapy.Field()
    game_date_time_utc = scrapy.Field()
    # home/away team
    home_team = scrapy.Field()
    away_team = scrapy.Field()
    # Area info
    arena_city = scrapy.Field()
    arena_state = scrapy.Field()
    arena_name = scrapy.Field()
    # Game id
    game_id = scrapy.Field()
