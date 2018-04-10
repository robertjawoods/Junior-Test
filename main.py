# Required Functionality:
# List leaderboard
# Record matches
# Add players

import ranking
import os.path
import logging

# Configure logging for easier debugging 
logger = logging.getLogger("elo_ranking_interface")
logging.basicConfig(level=logging.INFO)

def try_load_leaderboard():
     try: 
         os.path.isfile("leaderboard.txt")
     except:
         logger.info("Unable to find log file")
         return None
