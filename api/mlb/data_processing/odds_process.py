BOOKER1 = "fanduel"
BOOKER2 = "draftkings"
BOOKER3 = "betmgm"

class OddsProcessor:
    """
    A class to process and sort homerun odds by bookmaker.
    """

    @staticmethod
    def sort_homerun_odd_by_booker(event):
        """
        Sorts homerun odds by the specified bookmakers.

        Args:
            event (dict): The event data containing bookmaker odds.

        Returns:
            dict: A dictionary with bookmaker keys and their corresponding player homerun odds.
        """
        # Initialize the dictionary to hold processed data
        processed_data = {
            BOOKER1: {},
            BOOKER2: {},
            BOOKER3: {}
        }

        # Loop through the bookmakers in the event
        for bookmaker in event['bookmakers']:
            # Check if the bookmaker is one of the specified ones
            if bookmaker['key'] in [BOOKER1, BOOKER2, BOOKER3]:
                # Get the market data (assuming there's only one market per bookmaker)
                market = bookmaker['markets'][0]
                # Loop through the outcomes in the market
                for outcome in market['outcomes']:
                    # Check if the outcome is for 'Over' 0.5 homeruns
                    if outcome['name'] == 'Over' and outcome['point'] == 0.5:
                        # Add the outcome description (player name) and price to the processed data
                        processed_data[bookmaker['key']][outcome['description']] = outcome['price']

        return processed_data
