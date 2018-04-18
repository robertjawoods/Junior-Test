import ranking

class Match():
    def __init__(self):
        self.__scores = ()

    def record_score(self, playerName, score):
        self.__scores += ((playerName, score),)

    def get_match_results(self):
        return self.__scores

    def __str__(self):
        result = ""
        count = 1

        for (player1, points1), (player2, points2), in ranking.pairwise(self.__scores):
            result += f"Match {count} - {player1}: {points1} - {player2}: {points2}"

            count += 1

        return result