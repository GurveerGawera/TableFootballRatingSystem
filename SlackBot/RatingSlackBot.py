from typing import Text
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from RatingHandler import RatingHandler
from PlayerTracker import Player
from Teams import Team
import json

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

NEW_PLAYER_RATING = 1500.0

#TODO(Gurveer): Initialize at 1.5k rating, then store information about everyones ratings and use that in the future.
#TODO(Gurveer): Improve slack interface. e.g. allow for top 10 elo ratings to be printed when a command is called.
#TODO(Gurveer): Find a network to host the bot on.

# Load environment
load_dotenv()

# Setup local server
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", app)

# Setup Slack Bot
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]

PLAYER_INFORMATION = "player_information.txt"

@slack_event_adapter.on('message')
def message(payLoad):
    """
    Main script should accept the following format: player_name1 player_name2 player_name3 player_name4 score_of_game
    Team 1 will contain player_name1 and player_name2, Team 2 will contain player_name3 and player_name4
    Example input: @Gurveer @Raj @Davinder @Preet 10-5
    """
    event = payLoad.get('event', {})

    channel_id = event.get("channel") 
    user_id = event.get("user")

    if channel_id != "C02JV0GPC9Y" or user_id == BOT_ID: # maybe channel_name != #slack-bot
        return

    # Get the input and parse it.    
    input = event.get("text")
    input_strip = input.replace("<", "")
    input_strip = input_strip.replace(">", "")
    input_strip = input_strip.replace("@", "")
    input_split = input_strip.split()

    if len(input_split) != 5: # TODO(Gurveer): No magic numbers
        client.chat_postMessage(channel=channel_id, text="Please enter a valid input. Example input: \n@Gurveer @Raj @Davinder @Preet 10-5")
        return

    player_information = open(os.path.join(__location__, 'player_information.json'))
    player_data: dict = json.load(player_information)
    player_information.close()

    players: list[Player] = []

    # Parse player input.
    for index, player_slack_id in enumerate(input_split[0:4]):

        try:
            player_slack_id = client.users_info(user=player_slack_id) # TODO(Gurveer): Send chat message if player_id is not found.
            name = player_slack_id["user"]["real_name"]
        except:
            client.chat_postMessage(channel=channel_id, text="Please provide a valid input. Example input: \n@Gurveer @Raj @Davinder @Preet 10-5")
            return

        if name not in player_data:
            player_data[name] = NEW_PLAYER_RATING

        player = Player(name, player_data[name])
        players.append(player)

    rating_handler = RatingHandler(K=10)

    team1 = Team(players[0], players[1])
    team2 = Team(players[2], players[3])
    
    for x in range(1):

        # Play game and obtain new ratings for players in both teams.
        ratings = rating_handler.update_rating(team1, team2, input_split[4])

        players: list[Player] = team1.get_players() + team2.get_players()
        
        # Update player rating values.
        for index, player in enumerate(players):
            player.update_rating(ratings[index], player_data)

        with open(os.path.join(__location__, 'player_information.json'), 'w') as player_information:
            json.dump(player_data, player_information)


    client.chat_postMessage(channel=channel_id, text=f"Team 1: \n     {players[0].get_name()} : {players[0].print_rating()} \n     {players[1].get_name()} : {players[1].print_rating()} \nTeam 2: \n\
     {players[2].get_name()}: {players[2].print_rating()} \n     {players[3].get_name()} : {players[3].print_rating()}")

if __name__ == "__main__":
    app.run(debug=True)