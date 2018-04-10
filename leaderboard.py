import player

class Leaderboard:

    def __init__(self):
        self.rankings = []

    def addPlayer(player):
        self.rankings.insert(getPlayerPosition(player), player)

    def getPlayerPosition(player):
        position = 0

        for p in self.rankings:
            if p.eloRanking > player.eloRanking:
                position++

            if p.eloRanking <= player.eloRanking:
                return position
