class Player:

    def __init__(self, name, eloRanking):
        self.name = name
        self.eloRanking = eloRanking

        self.matchHistory = []

    def __str__(self):
        return f"Name: {self.name} - Elo Ranking: {self.eloRanking}"

    def add_match_to_history(self, match):
        self.matchHistory.append(match)

    def get_match_history(self):
        for m in self.matchHistory:
            print(m)