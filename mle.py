from collections import defaultdict
from lloss import logloss
from random import sample
import time



EPSILON = .01
# YEAR = sample([str(i) for i in range(1990, 2017)], 1)[0]
YEAR = '2004'
PATIENCE = 1000

def win_likelihood(p1, p2):
	return (p1 * (1 - p2) /
		(p1 * (1 - p2) + p2 * (1 - p1)))

# various_ratings = []
# TEST = 10

# for i in range(TEST):

# wteam, lteam
games = []

# get indices of games in which team participates
game_indices_by_team = {}

# for calculating initial estimates
wins_for_team = defaultdict(int)
losses_for_team = defaultdict(int)
teams = set()

with open('../madness/input/RegularSeasonCompactResults.csv') \
		as fp:
	next(fp)
	for line in fp:
		year, day, wteam, wscore, lteam, lscore, wloc, numot = line.strip().split(',')
		if year == YEAR:
			games.append((wteam, lteam))
			if not wteam in game_indices_by_team:
				game_indices_by_team[wteam] = set()
			if not lteam in game_indices_by_team:
				game_indices_by_team[lteam] = set()
			this_game = len(games) - 1
			game_indices_by_team[wteam].add(this_game)
			game_indices_by_team[lteam].add(this_game)
			wins_for_team[wteam] += 1
			losses_for_team[lteam] += 1

# (winner, loser)
tourney_outcomes = []
with open('../madness/input/TourneyCompactResults.csv') \
		as fp:
	next(fp)
	for line in fp:
		year, day, wteam, wscore, lteam, lscore, wloc, numot = line.strip().split(',')
		if year == YEAR:
			tourney_outcomes.append((wteam, lteam))

ratings = {}

for team in game_indices_by_team:
	ratings[team] = float(wins_for_team[team]) / (wins_for_team[team] + losses_for_team[team])

# loop to fit MLEs
start = time.time()
actual = [1] * len(games)
prediction = []
for wteam, lteam in games:
	prediction.append(win_likelihood(ratings[wteam], ratings[lteam]))

curr_ll, best_ll = 10, 10
convergence = 0
while convergence < PATIENCE:
	team = sample(ratings, 1)[0]
	provisional_rating = ratings[team] + (sample([1, -1], 1)[0] * EPSILON)
	provisional_prediction = prediction[:]
	for game_idx in game_indices_by_team[team]:
		if team == games[game_idx][0]:	
			provisional_prediction[game_idx] = win_likelihood(provisional_rating, ratings[games[game_idx][1]])
		else:
			provisional_prediction[game_idx] = win_likelihood(ratings[games[game_idx][0]], provisional_rating)
	curr_ll = logloss(actual, provisional_prediction)
	if curr_ll >= best_ll:
		convergence += 1
	else:
		best_ll = curr_ll
		ratings[team] = provisional_rating
		for game_idx in game_indices_by_team[team]:
			prediction[game_idx] = provisional_prediction[game_idx]
		convergence = 0

# add home-game advantage! say it improves win likelihood by N percent

# validation
actual = [1] * len(tourney_outcomes)
predicted = []
for wteam, lteam in tourney_outcomes:
	predicted.append(win_likelihood(ratings[wteam], ratings[lteam]))
curr_ll = logloss(actual, predicted)
print YEAR, 'score: ', curr_ll
print time.time() - start, " seconds to converge."

# 	various_ratings.append(ratings)

# with open("test.xls", "w") as fp:
# 	for team in various_ratings[0]:
# 		fp.write(team)
# 		for i in range(TEST):
# 			fp.write('\t' + str(various_ratings[i][team]))
# 		fp.write('\n')