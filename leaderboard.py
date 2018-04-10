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

    # Position in leaderboard, ie. 1st, 2nd. Array is 0 indexed so position - 1
    def get_player_by_position(self, position):
        return self.rankings[position - 1]

    # In a large leaderboard, a linear search could take a while. As this is so small, anything else seems like it'd be overkill
    def __get_player_by_name(self, name):
        for p in self.rankings:
            if p.name == name:
                return p

        return None

    def get_league_rankings(self):
        leagueRankings = {}

        for p in self.rankings:
            leagueRankings[p.name] = p.eloRanking

        return leagueRankings