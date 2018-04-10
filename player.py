class Player:

    def __init__(self, name, eloRanking):
        self.name = name
        self.eloRanking = eloRanking

    def __str__(self):
        return f"Name: {self.name} - Elo Ranking: {self.eloRanking}"