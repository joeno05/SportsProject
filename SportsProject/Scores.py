import json
import requests
from rich import print  # type: ignore

class Scores:
    def __init__(self, league_input: str, endpoints: dict):
        self.league_input = league_input
        self.endpoints = endpoints

    def fetchGameData(self, game_choice: str, data: dict) -> None:    
        game_index = int(game_choice) - 1  # Convert the game_choice to an index
        selected_game = data.get("events", [])[game_index]  # Get the selected game
        print("\nFull Game Data:")
        print(json.dumps(selected_game, indent=4))  # Pretty print the game data

    def printScores(self):
        match self.league_input:
                case "exit":
                    print("Exiting program.")
                    exit()
                case "nfl" | "nba" | "mlb" | "cfb" | "cfp" | "cbb" | "nhl" | "ucl" | "epl":
                    # Fetch the appropriate endpoint
                    url = self.endpoints[self.league_input]
                    try:
                        response = requests.get(url)
                        response.raise_for_status()  # Raises an error for bad HTTP responses
                        data = response.json()

                        print(f"You chose {self.league_input.upper()}. Here are the games color coded by channel:")
                        
                        # Game of the Day/Week
                        maxSumOfWins = 0
                        gameofthedayhometeam = ""
                        for i, event in enumerate(data.get("events", [])):
                            game_name = event.get("name", "No name available")
                            event_competitions = event.get("competitions", [])
                            event_competitors = event_competitions[0].get("competitors", []) if event_competitions else []

                            # Team Name Details
                            homeTeam = event_competitors[0].get("team", "NaN") if event_competitors else "NaN"
                            homeTeamName = homeTeam.get("displayName", "NaN") if homeTeam else "NaN"
                            awayTeam = event_competitors[1].get("team", "NaN") if len(event_competitors) > 1 else "NaN"
                            awayTeamName = awayTeam.get("displayName", "NaN") if awayTeam else "NaN"
                            
                            # Team Record Details
                            homeRecordData = event_competitors[0].get("records", None) if event_competitors else None
                            if homeRecordData:
                                homeRecord = homeRecordData[0]["summary"]
                                homeRecordArray = homeRecord.split("-")
                            else:
                                homeRecord = None

                            awayRecordData = event_competitors[1].get("records", None) if event_competitors else None
                            if awayRecordData:
                                awayRecord = awayRecordData[0]["summary"]
                                
                                awayRecordArray = awayRecord.split("-")
                            else:
                                awayRecord = None


                            if homeRecordArray and awayRecordArray:
                                sumOfWins = int(homeRecordArray[0]) + int(awayRecordArray[0])
                            else:
                                sumOfWins = 0

                            if "South Dakota" in awayTeamName:
                                sumOfWins = 0

                            if sumOfWins > maxSumOfWins:
                                maxSumOfWins = sumOfWins
                                gameofthedayhometeam = homeTeam
                        
                        # Display the games to the user
                        for i, event in enumerate(data.get("events", [])):
                            game_name = event.get("name", "No name available")
                            game_date = event.get("date", "No date available")
                            event_status = event.get("status", {})
                            event_type = event_status.get("type", {})
                            event_time = event_type.get("detail", "No time available")
                            status_state = event_type.get("state", "Game status error")
                            event_competitions = event.get("competitions", [])
                            event_competitors = event_competitions[0].get("competitors", []) if event_competitions else []
                            neutral_site = event_competitions[0].get("neutralSite", []) if event_competitions else []

                            # College Seeds Details
                            home_curatedRank = event_competitors[0].get("curatedRank", {}) if len(event_competitors) > 0 else {}
                            away_curatedRank = event_competitors[1].get("curatedRank", {}) if len(event_competitors) > 1 else {}

                            homeRank = str(home_curatedRank.get("current", ""))
                            awayRank = str(away_curatedRank.get("current", ""))

                            if homeRank == "99":
                                homeRank = ""
                            if awayRank == "99":
                                awayRank = ""

                            # Team Name Details
                            homeTeam = event_competitors[0].get("team", "NaN") if event_competitors else "NaN"
                            homeTeamName = homeTeam.get("displayName", "NaN") if homeTeam else "NaN"
                            awayTeam = event_competitors[1].get("team", "NaN") if len(event_competitors) > 1 else "NaN"
                            awayTeamName = awayTeam.get("displayName", "NaN") if awayTeam else "NaN"

                            if "South Dakota" in awayTeamName:
                                continue

                           # Team Record Details
                            homeRecordData = event_competitors[0].get("records", None) if event_competitors else None
                            if homeRecordData:
                                homeRecord = homeRecordData[0]["summary"]
                            else:
                                homeRecord = None
                            awayRecordData = event_competitors[1].get("records", None) if event_competitors else None
                            if awayRecordData:
                                awayRecord = awayRecordData[0]["summary"]
                            else:
                                awayRecord = None

                            # Notes details
                            event_notes = None
                            headline_data = None

                            if event_competitions and "notes" in event_competitions[0]:
                                notes_data = event_competitions[0]["notes"]
                                
                                # Check if notes_data is a non-empty list and contains the "headlines" key
                                if isinstance(notes_data, list) and notes_data and "headline" in notes_data[0]:
                                    headline_data = notes_data[0]["headline"]

                                # Check if headline_data is a dictionary and retrieve the "name" key
                                if isinstance(headline_data, dict):
                                    event_notes = headline_data.get("name", None)
                                elif headline_data:  # If headline_data is not a dictionary but exists
                                    event_notes = headline_data

                            if self.league_input == "cfp":
                                if "College Football Playoff" not in event_notes:
                                    i -= 1
                                    continue

                            # Broadcast details
                            event_broadcast = "No broadcast available"
                            if event_competitions and "broadcast" in event_competitions[0]:
                                broadcast_data = event_competitions[0]["broadcast"]
                                if isinstance(broadcast_data, dict):  # Ensure broadcast_data is a dictionary
                                    event_broadcast = broadcast_data.get("name", "No broadcast available")
                                else:
                                    event_broadcast = broadcast_data  # Use the string if it's not a dictionary

                            # Headline details
                            event_headline = None
                            if event_competitions and "highlights" in event_competitions[0] and "highlights"[0] != None:
                                highlights = event_competitions[0]["highlights"]
                                if highlights and "headline" in highlights[0]:
                                    event_headline = highlights[0]["headline"]
                            else:
                                if event_competitions and "headlines" in event_competitions[0]:
                                    headlines = event_competitions[0]["headlines"]
                                    if headlines and "shortLinkText" in headlines[0]:
                                        event_headline = headlines[0]["shortLinkText"]

                            # Scores
                            final_scoreH = event_competitors[0].get("score", "NaN") if event_competitors else "NaN"
                            final_scoreA = event_competitors[1].get("score", "NaN") if len(event_competitors) > 1 else "NaN"
                            
                            # Define hex colors for each broadcast type
                            colorByBroadcast_map = {
                                "Prime Video": "#FFFFFF", #White
                                "CBS": "#1E90FF",  # Dodger Blue
                                "FOX": "#FFD700",  # Gold
                                "FS1": "#FFD700",  # Gold
                                "NBC": "#32CD32",  # Lime Green
                                "ESPN": "#FF4500",  # Orange Red
                                "ABC": "#FF4500",  # Orange Red
                                "TNT": "#1E90FF",  # Dodger Blue
                                "TBS": "#1E90FF",  # Dodger Blue
                                "NBA TV": "#FFD700",  # Gold
                                "NHL Net": "#FFD700"  # Gold
                            }
                            if event_broadcast in colorByBroadcast_map:
                                color = colorByBroadcast_map[event_broadcast]
                            elif self.league_input == {"ucl", "nhl"}:
                                color = "#03befc" # Light Blue
                            else:
                                color = "#FFFFFF"  # Default color
                                for key, hex_color in colorByBroadcast_map.items():
                                    if key in event_broadcast:
                                        color = hex_color
                                        break  # Stop at the first match
                            
                            # Generate game name with conditional spaces after ranks
                            game_name = f"{awayRank + ' ' if awayRank else ''}{awayTeamName}{"(" + awayRecord + ")" if awayRecord else ''} {"vs" if neutral_site else "at"} {homeRank + ' ' if homeRank else ''}{homeTeamName}{"(" + homeRecord + ")" if homeRecord else ''}"

                            if event_notes:
                                game_name += f" ({event_notes})"

                            if homeTeam == gameofthedayhometeam:
                                game_name += f" (GAME OF THE {"WEEK" if self.league_input == "nfl" or self.league_input == "cfb" or self.league_input == "cfp" else "DAY"})"    
                            
                            # Determine color based on status and rank presence
                            if status_state == "post":
                                color = "#FFFFFF"  # White for completed games
                            formatted_game = f"[{color}]{i+1}. {game_name}[/]"

                            # Print formatted game
                            print(formatted_game)

                            #everything else
                            if status_state == "pre":
                                print(f"\tTime: {event_time}")
                                if event_broadcast != "":
                                    print(f"\tNational TV: {event_broadcast}")
                            elif status_state == "post":
                                print(f"\tFinal Score: {final_scoreA} at {final_scoreH}")
                                if event_headline:
                                    print(f"\tHeadline: {event_headline}")        
                            else: #game in progress
                                print(f"[#FF4500]\tScore: {final_scoreA} at {final_scoreH}")
                                print(f"[#FF4500]\tTime: {event_time} ⦿")
                                if event_broadcast != "":
                                    print(f"[#FF4500]\tNational TV: {event_broadcast}[/]")

                        """
                        # Ask the user to select a game or type 'exit' to quit
                        game_choice = input("\nEnter the number of the game to see leaders and odds, 0 to continue or type 'exit' to quit:\n\t")
                        gamePage(game_choice, self.league_input)

                        # Press any key to continue    
                            
                        """
                        # Ask the user to select a game or type 'exit' to quit
                        game_choice = input("\nEnter the number of the game to dump all data, or type 'exit' to quit:\n\t")
                        if game_choice.lower() == "exit":
                            print("Exiting program.")
                            exit()
                        if game_choice.lower() == "0":
                            return
                            
                        # Convert choice to index and display the selected game data
                        try:
                            self.fetchGameData(game_choice, data)
                        except (ValueError, IndexError):
                            print("Invalid game number. Please try again.")
                        
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching data for {self.league_input.upper()}: {e}")
                case "live now":
                    print("Unfinished")

                case _:
                    print("Invalid option. Please choose a valid league (NFL, NBA, MLB, CFB, CFP (CFB Playoff), CBB, NHL, UCL, EPL).")
