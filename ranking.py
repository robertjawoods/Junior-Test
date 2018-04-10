"""
Logic for the calculation of Elo ranking scores.

Was made referring to METIN'S MEDIA & MATH: HOW TO CALCULATE THE ELO-RATING
"""
import logging
from collections import defaultdict
from itertools import tee

# Found out online that izip only needs to be imported when using python 2. 
# I'm using python 3 so rather than change izip to zip, give zip the alias 'izip'
try: 
    from itertools import izip
except ImportError:
    izip = zip

SIGMA = 400.  # type: float
K_FACTOR = 32  # 32 is suggested on Metin's Media & Math

INITIAL_RATING = 1200

logger = logging.getLogger("elo_ranking")
logging.basicConfig(level=logging.INFO)

def transform_rating(elo_score):
    """
    Compute the transformed (exponentiated) rating for each player or team
    :type elo_score: float
    :return: transformed ratings
    """
    return 10. ** (elo_score / SIGMA)


def calc_expected_score(p1_elo_score, p2_elo_score):
    """
    calculate expected results (win probability) for pair of players based on elo score
    :type p1_elo_score: float
    :type p2_elo_score: float
    :return: win probability of the two players
    :rtype: (float, float)
    """
    p1_rating = transform_rating(p1_elo_score)
    p2_rating = transform_rating(p2_elo_score)

    e1 = p1_rating / (p1_rating + p2_rating)
    e2 = p2_rating / (p1_rating + p2_rating)

    return (e1, e2)


def pairwise(iterable):
    """ s -> (s0,s1), (s1,s2), (s2, s3), ...
    recipe from the python itertools docs """
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def gen_win_pairs_from_result(performances):
    """
    Following Tom Kerrigan's Simple Multiplayer Elo. In a mutliplayer game, the intermediate players,
    (players who did not come top or bottom) are treated to have played two games, one with the
    person right above him/her on the performance list, and another with the person right below him/her.
    A win is 1 point, a draw 0.5 points, and a loss 0. points.
    :param tuple[(str, float | int)] performances:
    :return: k-1 pairs of win results
    """

    perfs_descending = sorted(performances, key=lambda x: x[1], reverse=True)

    two_player_game_results = []

    # iterate through pairs, getting 2-player match results
    for (player1, points1), (player2, points2), in pairwise(perfs_descending):

        if points1 > points2:
            two_player_game_results.append((player1, player2, 1))
        elif points1 == points2:
            two_player_game_results.append((player1, player2, 0.5))
        else:
            raise ValueError("performances weren't in descending order! requires debug")

    return two_player_game_results


def calc_multiplayer_updates(performances, player_elos):

    init_any_new_players(performances, player_elos)

    updates = defaultdict(list)
    for player_a, player_b, result in gen_win_pairs_from_result(performances):
        expected_a, expected_b = calc_expected_score(player_elos[player_a], player_elos[player_b])
        result_a = result
        result_b = 1 - result

        updates[player_a].append(K_FACTOR * (result_a - expected_a))
        updates[player_b].append(K_FACTOR * (result_b - expected_b))

    return updates


def init_any_new_players(performances, elo_scores):
    """
    queries the user whether to add previously unseen player names (if any) in the performances input
    doesn't just add automatically because the user could have made a typo
    new players are initialised to the default starting score.
    :param performances: player performances in the current game
    :param elo_scores: previously recorded scores
    :return: None (scores are stored in dict (mutable) so no need to return them)
    """

    def get_user_input(player_name):
        return raw_input("do you want to add %s as new player? (y/n)" % player_name)

    for (player_name, _) in performances:
        if player_name not in elo_scores.keys():
            user_input = get_user_input(player_name)
            while not user_input.startswith(('y', 'Y', 'n', 'N')):
                user_input = get_user_input(player_name)
            if user_input[0].lower() == 'n':
                raise ValueError("unable to proceed - no record for player '%s'" % player_name)

            # add new player
            logger.info("adding new player '%s' with initial elo rating %g" % (player_name, INITIAL_RATING))
            elo_scores[player_name] = INITIAL_RATING



def apply_multiplayer_updates(performances, player_elos):

    all_updates = calc_multiplayer_updates(performances, player_elos)
    updated_elos = player_elos.copy()
    for player_name, player_updates in all_updates.items():
        total_update = sum(player_updates)
        updated_elos[player_name] += total_update
        logger.info("%s's new Elo score: %.3f (%+.3f)" % (player_name, updated_elos[player_name], total_update))
    return updated_elos