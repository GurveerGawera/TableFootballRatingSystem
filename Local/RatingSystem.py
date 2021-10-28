from PlayerTracker import Player
from RatingHandler import RatingHandler
from Teams import Team
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

NEW_PLAYER_RATING = 1500.0

def main():

    # Main script should accept the following format: player_name1 player_name2 player_name3 player_name4 score_of_game
    # Team 1 will contain player_name1 and player_name2, Team 2 will contain player_name3 and player_name4
    # Example input: Gurveer Raj Davinder Preet 10-5

    player_information = open(os.path.join(__location__, 'player_information.json'))
    player_data: dict = json.load(player_information)
    player_information.close()

    input = "@Gurveer @Raj @Davinder @Preet 10-5"
    input_split = input.split(" ")

    players: list[list[str, int]] = []

    # Parse player input.
    for index, name in enumerate(input_split[0:4]):
        if name not in player_data:
            player_data[name] = NEW_PLAYER_RATING

        player = Player(name, player_data[name])
        players.append(player)

    rating_handler = RatingHandler(K=10)


    team1 = Team(players[0], players[1])
    team2 = Team(players[2], players[3])

    team_one_win = True
    
    for x in range(10):


        if team_one_win:
            temp = "10-5"
        else:
            temp = "5-10"
        print("score = ", temp)

        # Play game and obtain new ratings for players in both teams.
        ratings = rating_handler.update_rating(team1, team2, temp)
        print("ratings after game: ", ratings)

        players: list[Player] = team1.get_players() + team2.get_players()
     
        # Update player rating values.
        for index, player in enumerate(players):
            player.update_rating(ratings[index], player_data)

        with open(os.path.join(__location__, 'player_information.json'), 'w') as player_information:
            json.dump(player_data, player_information)
        
        team_one_win = not(team_one_win)

    

    # print("Team 1 ratings : \n Gurveer: {0} \n Raj: {1} \n Davinder: {2} \n Preet: {3} \n Games played {4} \n rating history for Gurveer: {5}" \
    #     .format(player1.get_rating(), player2.get_rating(), player3.get_rating(), player4.get_rating(), player4.get_games_played(), player1.get_rating_history()))
    

if __name__ == "__main__":
    main()