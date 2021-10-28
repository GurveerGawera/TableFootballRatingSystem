class Player(object):
    """
    Class to hold information about the player.
    """
    def __init__(self, name: str, rating: float):  
        """
        :param name: player name.
        :param rating: initialize a rating to start at for the player.
        """
        assert type(name) == str
        assert type(rating) == float
        if rating < 1:
            raise ValueError("Rating ({0}) input must be a positive integer.".format(rating))

        self.__name = name
        self.__rating = rating
        # TODO(Gurveer): Visuailize the rating history.

    def update_rating(self, rating_value, player_data):
        """
        Update the rating for the player, generally after a game has been played.
        :param rating_value: rating value to update
        :param player_data: data for all players.
        """
        assert type(rating_value) == float
        assert type(player_data) == dict

        player_data[self.get_name()] = rating_value

    def get_rating(self) -> float:
        """
        :return rating: Return the rating for the player
        """
        return self.__rating

    def get_name(self) -> str:
        """
        :return name: The name of the player.
        """
        return self.__name
