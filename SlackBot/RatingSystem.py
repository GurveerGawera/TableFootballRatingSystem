from PlayerTracker import Player
from RatingHandler import RatingHandler
from Teams import Team
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

NEW_PLAYER_RATING = 1500

def main():

    # Main script should accept the following format: player_name1 player_name2 player_name3 player_name4 score_of_game
    # Team 1 will contain player_name1 and player_name2, Team 2 will contain player_name3 and player_name4
    # Example input: Gurveer Raj Davinder Preet 10-5

    input = "@Gurveer @Raj @Davinder @Preet 10-5"

    input_split = input.split(" ")

    player1 = Player(input_split[0])
    player2 = Player(input_split[1])
    player3 = Player(input_split[2])
    player4 = Player(input_split[3])

    rating_handler = RatingHandler(K=10)

    team1 = Team(player1, player2)
    team2 = Team(player3, player4)
    
    for x in range(10):

        # Play game and obtain new ratings for players in both teams.
        ratings = rating_handler.update_rating(team1, team2, input_split[4])

        players: list[Player] = team1.get_players() + team2.get_players()
        
        # Update player rating values.
        for index, player in enumerate(players):
            player.update_rating(ratings[index])

    print("Team 1 ratings : \n Gurveer: {0} \n Raj: {1} \n Davinder: {2} \n Preet: {3} \n Games played {4} \n rating history for Gurveer: {5}" \
        .format(player1.get_rating(), player2.get_rating(), player3.get_rating(), player4.get_rating(), player4.get_games_played(), player1.get_rating_history()))
    

if __name__ == "__main__":
    main()