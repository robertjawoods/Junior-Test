import ranking

class Match():
    def __init__(self):
        self.__scores = {}

    def record_score(self, playerName, score):
        self.__scores[playerName] = score

    def get_match_results(self):
        return self.__scores
