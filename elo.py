import math

######################################
# sequential ELO rankings suffer from poor data capture
# they do not capture full-season effects and converge slowly
# they impose narrative arcs unnecessarily
# I want a regular-season metric to apply to playoffs
######################################

# ((team_a, score_a), (team_b, score_b))
games = []
with open('../kaggle/madness/input/RegularSeasonCompactResults.csv') \
		as fp:
	next(fp)
	for line in fp:
		year, day, wteam, wscore, lteam, lscore, wloc, numot = line.strip().split(',')
		if year == '2004':
			games.append(((wteam, int(wscore)), (lteam, int(lscore))))


def expected(a_rat, b_rat):
	# print a_rat, b_rat, 1 / (math.exp((a_rat - b_rat) / 100) + 1)
	return 1 / (math.exp((b_rat - a_rat) / 1000) + 1)

# should be in the ballpark of 24; maybe 100 for bad/new players, 10 for absolute pros
def K(rating):
	return 100

def new_rat(a_rat, b_rat, result):
	return a_rat + K(a_rat) * (result - expected(a_rat, b_rat))

rating = {}
for (a_nm, a_sc), (b_nm, b_sc) in games:
	if not a_nm in rating:
		rating[a_nm] = 1600
	if not b_nm in rating:
		rating[b_nm] = 1600
	a_win = 1 if a_sc > b_sc else (0 if b_sc > a_sc else .5)
	if a_nm == '1360' or b_nm == '1360':
		print a_nm, rating[a_nm], a_sc, b_nm, rating[b_nm], b_sc
		if a_nm == '1360':
			print a_win, expected(rating[a_nm], rating[b_nm])
		else:
			print (1 - a_win), expected(rating[b_nm], rating[a_nm])
	rating[a_nm] = new_rat(rating[a_nm], rating[b_nm], a_win)
	rating[b_nm] = new_rat(rating[b_nm], rating[a_nm], 1 - a_win)


print rating