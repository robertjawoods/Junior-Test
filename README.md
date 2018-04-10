This challenge involves taking some existing code and modifying it to ensure that it meets a given set of criteria. Once you are happy with your solution please send it back to us, either by uploading it to a publicly accessible code repository (e.g. Github) or email it directly to us in the form of a zip archive.

The Elo rating system is a way of calculating the level of skill of a player in games such as chess. The Elo rating of a player takes the form of a number that is recalculated every time that player plays a match against another Elo ranked player. After a match the winning player's takes rating points from the losing player, with the amount of points taken determined by the difference between the two players' rating before the match. (see https://en.wikipedia.org/wiki/Elo_rating_system)

The supplied python module `ranking.py` contains functions for calculating the Elo rankings of players following a match. Running the file from the command line gives a clue as to how those functions can be used. We would like you to write a simple interface to interact with these functions and manage a league of players of a specific type of game. The interface should store and retrieve match results, players and their scores. The interface you implement can be a command line interface, a graphical web interface or HTTP API.

The interface should support the following functionality:
1. Recalculate and store the Elo rating of players by entering the results of a single match.
2. Retrieve a summary of current players and their ranking in the league based on their Elo rating.

NB: It is only necessary to support a single league of players that play one type of game only.
