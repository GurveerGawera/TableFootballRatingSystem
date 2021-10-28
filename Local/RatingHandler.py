from Teams import Team


class RatingHandler(object):
    """
    Class to handle the rating change after a game between players.
    """
    def __init__(self, K: int = 10):
        """
        :param K: Constant for calculating how much rating is gained/lost from a game. Bigger K value, bigger rating ajustment per game.
        """
        self.__K = K
        self.__D = 400

    def expected_score(self, team_one: float, team_two: float) -> float:   
        """
        Calculate the expected score between two players.
        Expected score is the percentage change (e.g. 0.76) of player_one winning.

        :param team_one: Player 1 rating
        :param team_two: Player 2 rating
        """
        return 1 / (1 + 10**((team_two - team_one)/self.__D))

    def adjust_rating(self, player_rating: float, expected_score: float, team_one_win: bool, team_index: int, score_difference: int) -> float:
        """
        Adjust the rating for a single player depending on expected score and which team won.

        :param player_rating: Rating of the player before the game
        :param expected_score: expected score for the game, given the players ratings on each team
        :param team_one_win: True if team one won the game, False otherwise
        :param team_index: The team value, which the player is on. e.g. Team 1 = 0, Team 2 = 1
        :param score_difference: The difference in score between the two teams. e.g. 10-5, score_difference = 5
        :returns player_rating: Rating for the player after the game
        """
        if team_index == 0:
            if team_one_win:
                player_rating += ((self.__K + score_difference) * (1 - expected_score))
            else:
                player_rating += ((self.__K + score_difference) * (0 - expected_score))
        else:
            if team_one_win:
                player_rating -= ((self.__K + score_difference) * (1 - expected_score))
            else:
                player_rating -= ((self.__K + score_difference) * (0 - expected_score))

        return player_rating

    def parse_score(self, score: str) -> tuple[bool, int]:
        """
        Function used to parse the inputted score from user.
        :param score: Score, winning team has 10 points. Should be in the format: "int-int" e.g. 10-5
        :return team_one_win: True if team one wins, False otherwise
        """
        assert len(score) == 4

        score_split = score.split("-")

        assert score_split[0].isdigit()
        assert score_split[1].isdigit()

        team_one_points = int(score_split[0])
        team_two_points = int(score_split[1])

        assert team_one_points <= 10 and team_one_points >= 0
        assert team_two_points <= 10 and team_two_points >= 0
        
        if team_one_points == 10:
            team_one_win = True
        else:
            team_one_win = False

        score_difference = abs(team_one_points - team_two_points)
        
        return team_one_win, score_difference


    def update_rating(self, team_one: Team, team_two: Team, score: str) -> list[float]:
        """
        Obtain the updated rating for each player.

        :param team_one: ratings for players in team 1
        :param team_two: ratings for players in team 2
        :param score: Score, winning team has 10 points. Should be in the format: "int-int" e.g. 10-5
        :returns: updated rating for each player
        """

        assert type(team_one) == Team
        assert type(team_two) == Team
        assert type(score) == str

        # Parse the score
        team_one_win, score_difference = self.parse_score(score)

        team_ratings: tuple[tuple[float, float], tuple[float, float]] = (team_one.get_player_ratings(), team_two.get_player_ratings())

        expected_score: float = self.expected_score(team_one.get_average_rating(), team_two.get_average_rating())

        updated_player_ratings: list[float] = []

        for index, team in enumerate(team_ratings):
            for player_ratings in team:
                adjusted_rating = self.adjust_rating(player_ratings, expected_score, team_one_win, index, score_difference)
                updated_player_ratings.append(adjusted_rating)
            
        return updated_player_ratings








