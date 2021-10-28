from PlayerTracker import Player

class Team(object): # Data class maybe?
    """
    Class for an instance of a team.
    """
    def __init__(self, player1: Player, player2: Player):
        """
        :param player1: first player of the team.
        :param player2: second player of the team.
        """
        self.__player1 = player1
        self.__player2 = player2

    def get_average_rating(self) -> float:
        """
        :returns: average rating for the team.
        """
        return (self.__player1.get_rating() + self.__player2.get_rating())/2

    def get_player_ratings(self) -> tuple[float, float]:
        """
        :returns: The players ratings in order.
        """
        return (self.__player1.get_rating(), self.__player2.get_rating())

    def get_players(self) -> list[Player]:
        """
        :returns: All players in team.
        """
        return [self.__player1, self.__player2]