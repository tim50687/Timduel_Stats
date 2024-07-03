
BOOKER1 = "fanduel"
BOOKER2 = "draftkings"
BOOKER3 = "betmgm"

class OddsProcessor:
    @staticmethod
    def sort_homerun_odd_by_booker(event):
        processed_data = {
              BOOKER1: {},
              BOOKER2: {},
              BOOKER3: {}
        }

        for bookmaker in event['bookmakers']:
            if bookmaker['key'] in [BOOKER1, BOOKER2, BOOKER3]:
                market =  bookmaker['markets'][0]
                for outcome in market['outcomes']:
                    if outcome['name'] == 'Over' and outcome['point'] == 0.5:
                        processed_data[bookmaker['key']][outcome['description']] = outcome['price']

        return processed_data                            

