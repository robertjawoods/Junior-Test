import player
import match
import ranking

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

    def update_elo(self, playerName, newElo):
        p = self.get_player_by_name(playerName)
        p.eloRanking = newElo

    def update_league_rankings(self):
        print("Not implemented")

    # In a large leaderboard, a linear search could take a while. As this is so small, anything else seems like it'd be overkill
    def get_player_by_name(self, name):
        for p in self.rankings:
            if p.name == name:
                return p

        return None

    def get_league_rankings(self, player1Name, player2Name):
        leagueRankings = {}

        leagueRankings[player1Name] = self.get_player_by_name(player1Name).eloRanking
        leagueRankings[player2Name] = self.get_player_by_name(player2Name).eloRanking

        return leagueRankings

    def recordMatch(self, player1Name, player1Score, player2Name, player2Score):
        game = match.Match()

        game.record_score(player1Name, player1Score)
        game.record_score(player2Name, player2Score)

        ranks = self.get_league_rankings(player1Name, player2Name)

        scores = game.get_match_results()
        updated_elo = ranking.apply_multiplayer_updates(scores, ranks)

        for k, v in updated_elo.items():
            self.update_elo(k, v)

        #self.update_league_rankings()