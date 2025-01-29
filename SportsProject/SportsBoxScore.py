from Scores import Scores # type: ignore
from rich import print  # type: ignore

def main():
    # API endpoints for different leagues
    endpoints = {
        "nfl": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
        "nba": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard",
        "mlb": "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard",
        "cfb": "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
        "cfp": "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
        "cbb": "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard",
        "nhl": "http://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard",
        "ucl": "http://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard",
        "epl": "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    }

    while True:
        # Ask the user to select a league or type 'exit' to quit
        print("[#1E90FF]Type a league (NFL, NBA, MLB, CFB, CFP (CFB Playoff), CBB, NHL, UCL, EPL) to see scores\nType 'Live Now' to see all live scores\nType 'exit' to quit:[/]")
        league_input = input("\t").lower()
        
        if league_input == "exit":
            print("Exiting program.")
            exit()

        # Create an instance of Scores and call the printScores method
        scores_instance = Scores(league_input, endpoints)
        scores_instance.printScores()

# Call the function
main()
