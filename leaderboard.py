import player

class Leaderboard():

    def __init__(self):
        self.rankings = []

    def get_player_position(self, player):
        position = 0

        if len(self.rankings) == 0:
            return 0

        for p in self.rankings:
            if p.eloRanking > player.eloRanking:
                position += 1
            elif p.eloRanking <= player.eloRanking:
               break

        return position
        
    def add_player(self, player):
        position = self.get_player_position(player)
        self.rankings.insert(position, player)

