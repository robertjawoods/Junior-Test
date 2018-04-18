import unittest
import itertools
import ranking
import player
import leaderboard
import json

if False:
    import collections

# example players
ALICE = 'alice'
BOB = 'bob'
CEVIN = 'cevin'
DOGE = 'doge'

def flatten(list_of_lists):
    """
    flatten function from itertools package - faster than list interpretation
    :type list_of_lists: collections.Iterable[collections.Iterable]
    :return:  chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
    """
    return itertools.chain.from_iterable(list_of_lists)

class TestRanking(unittest.TestCase):

    initial_elos = {ALICE: 1350, BOB: 1300, CEVIN: 1200, DOGE: 1600}
    result_2_players = ((ALICE, 404), (BOB, 200))
    result_4_players = ((ALICE, 404), (BOB, 200), (CEVIN, -100), (DOGE, 1000))

    def test_calc_expected_score(self):

        self.assertEqual(ranking.calc_expected_score(1000, 1000),    (0.5, 0.5))
        self.assertAlmostEquals(ranking.calc_expected_score(1000, 10000)[0], 0.)

    def test_gen_win_pairs_from_result(self):

        self.assertEqual(ranking.gen_win_pairs_from_result(self.result_2_players), [(ALICE, BOB, 1.)])
        self.assertEqual(ranking.gen_win_pairs_from_result(self.result_4_players),
                         [(DOGE, ALICE, 1.), (ALICE, BOB, 1.), (BOB, CEVIN, 1.)])

        # TODO: No test case for drawing scores, as undefined

    def test_multiplayer_updates(self):

        updates_2_player = ranking.calc_multiplayer_updates(self.result_2_players, self.initial_elos)
        # check number of updates as expected
        self.assertEqual(len(updates_2_player), 2)
        self.assertEqual(len(updates_2_player[ALICE]), 1)
        self.assertEqual(len(updates_2_player[BOB]), 1)
        # updates should sum to zero
        self.assertAlmostEquals(sum(flatten(updates_2_player.values())), 0)

        updates_4_player = ranking.calc_multiplayer_updates(self.result_4_players, self.initial_elos)
        # check number of updates as expected
        self.assertEqual(len(updates_4_player), 4)
        self.assertEqual(len(updates_4_player[DOGE]), 1)
        self.assertEqual(len(updates_4_player[ALICE]), 2)
        self.assertEqual(len(updates_4_player[BOB]), 2)
        self.assertEqual(len(updates_4_player[CEVIN]), 1)
        # updates should sum to zero
        self.assertAlmostEquals(sum(flatten(updates_4_player.values())), 0)

        # apply some updates
        updated_elos = ranking.apply_multiplayer_updates(self.result_4_players, self.initial_elos)
        self.assertEqual(updated_elos[ALICE], self.initial_elos[ALICE] + sum(updates_4_player[ALICE]))
        self.assertEqual(updated_elos[DOGE], self.initial_elos[DOGE] + sum(updates_4_player[DOGE]))
        self.assertAlmostEquals(sum(updated_elos.values()), sum(self.initial_elos.values()))


    def test_check_leaderboard_loads(self):
        # Arrange 
        rob = player.Player("Rob", 1200)
        zak = player.Player("Zak", 1200)

        board = leaderboard.Leaderboard()
        board.add_player(rob)
        board.add_player(zak)

        # Act 
        print(zak)
        print(rob)

        # Assert
        #self.assertEqual(main.try_load_leaderboard(), None)
        self.assertNotEqual(rob.name, zak.name)

    def test_check_leaderboard_is_in_order_start(self):
         # Arrange        
        cieran = player.Player("Cieran", 900)
        rob = player.Player("Rob", 1600)
        zak = player.Player("Zak", 1200)

        # Act 
        board = leaderboard.Leaderboard()
       
        board.add_player(cieran)
        board.add_player(zak)
        board.add_player(rob)

        # Assert
        self.assertEqual(board.rankings[0].name, "Rob")
        self.assertEqual(board.rankings[1].name, "Zak")
        self.assertEqual(board.rankings[2].name, "Cieran")

    def test_check_match_recording(self):
        # Arrange 
        rob = player.Player("Rob", 1200)
        zak = player.Player("Zak", 1200)

        board = leaderboard.Leaderboard()
        board.add_player(rob)
        board.add_player(zak)

        performances = [(rob.name, 1), (zak.name, 0)]

        testResults = ranking.calc_multiplayer_updates(performances, board.get_league_rankings(rob.name, zak.name))

        board.recordMatch(rob.name, 1, zak.name, 0)

        elo1 = board.get_player_by_name(rob.name).eloRanking
        elo2 = board.get_player_by_name(zak.name).eloRanking

        testElo1 = 1200 + testResults[rob.name][0]
        testElo2 = 1200 + testResults[zak.name][0]

        self.assertAlmostEqual(elo1, testElo1)
        self.assertAlmostEqual(elo2, testElo2)

    def test_match_history_recording(self):
        rob = player.Player("Rob", 1200)
        zak = player.Player("Zak", 1200)

        board = leaderboard.Leaderboard()
        board.add_player(rob)
        board.add_player(zak)

        board.recordMatch(zak.name, 1, rob.name, 0)

        self.assertEqual(len(rob.matchHistory), 1)
        self.assertEqual(len(zak.matchHistory), 1)

    def test_leaderboard_update(self):
        rob = player.Player("Rob", 1200)
        zak = player.Player("Zak", 1200)

        board = leaderboard.Leaderboard()
        board.add_player(rob)
        board.add_player(zak)

        board.recordMatch(zak.name, 1, rob.name, 0)

        self.assertEqual(board.rankings[0].name, zak.name)
        self.assertEqual(board.rankings[1].name, rob.name)

        board.recordMatch(zak.name, 0, rob.name, 1)
        board.recordMatch(zak.name, 0, rob.name, 1)

        self.assertEqual(board.rankings[0].name, rob.name)
        self.assertEqual(board.rankings[1].name, zak.name)
        

    if __name__ == '__main__': unittest.main()