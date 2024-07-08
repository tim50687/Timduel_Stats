import json

class PlayerStatsProcessor:
    team_names = {
        "ARI": "Arizona Diamondbacks",
        "ATL": "Atlanta Braves",
        "BAL": "Baltimore Orioles",
        "BOS": "Boston Red Sox",
        "CHC": "Chicago Cubs",
        "CHW": "Chicago White Sox",
        "CIN": "Cincinnati Reds",
        "CLE": "Cleveland Guardians",
        "COL": "Colorado Rockies",
        "DET": "Detroit Tigers",
        "HOU": "Houston Astros",
        "KCR": "Kansas City Royals",
        "LAA": "Los Angeles Angels",
        "LAD": "Los Angeles Dodgers",
        "MIA": "Miami Marlins",
        "MIL": "Milwaukee Brewers",
        "MIN": "Minnesota Twins",
        "NYM": "New York Mets",
        "NYY": "New York Yankees",
        "OAK": "Oakland Athletics",
        "PHI": "Philadelphia Phillies",
        "PIT": "Pittsburgh Pirates",
        "SDP": "San Diego Padres",
        "SEA": "Seattle Mariners",
        "SFG": "San Francisco Giants",
        "STL": "St. Louis Cardinals",
        "TBR": "Tampa Bay Rays",
        "TEX": "Texas Rangers",
        "TOR": "Toronto Blue Jays",
        "WSN": "Washington Nationals"
    }
    @staticmethod
    def load_json(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def combine_player_stats(statcast_data, stats_data):
        combined_data = {}
        for team, players in statcast_data.items():
            full_team_name = PlayerStatsProcessor.team_names[team]
            combined_data[full_team_name] = {}
            for player, stats in players.items():
                combined_data[full_team_name][player] = stats
                if team in stats_data and player in stats_data[team]:
                    combined_data[full_team_name][player].update(stats_data[team][player])
        return combined_data
    
    @staticmethod
    def get_complete_data(statcast_file, stats_file):
        statcast_data = PlayerStatsProcessor.load_json(statcast_file)
        stats_data = PlayerStatsProcessor.load_json(stats_file)
        return PlayerStatsProcessor.combine_player_stats(statcast_data, stats_data)


