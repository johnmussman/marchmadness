# ((team_a, score_a), (team_b, score_b))
games = []
with open('../madness/input/RegularSeasonCompactResults.csv') \
		as fp:
	next(fp)
	for line in fp:
		year, day, wteam, wscore, lteam, lscore, wloc, numot = line.strip().split(',')
		if year == '2004':
			games.append(((wteam, int(wscore)), (lteam, int(lscore))))



def win_likelihood(p1, p2):
	return (p1 * (1 - p2)) /
		(p1 * (1 - p2) + p2 * (1 - p1))
