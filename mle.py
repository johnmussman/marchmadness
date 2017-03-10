from collections import defaultdict

EPSILON = .01

# ((team_a, score_a), (team_b, score_b))
games = []

# for calculating initial estimates
wins_for_team = defaultdict(int)
losses_for_team = defaultdict(int)
teams = set()

with open('../madness/input/RegularSeasonCompactResults.csv') \
		as fp:
	next(fp)
	for line in fp:
		year, day, wteam, wscore, lteam, lscore, wloc, numot = line.strip().split(',')
		if year == '2004':
			games.append(((wteam, int(wscore)), (lteam, int(lscore))))
			wins_for_team[wteam] += 1
			losses_for_team[lteam] += 1
			teams.add(wteam)
			teams.add(lteam)

initials_for_team = {}
for team in teams:
	initials_for_team[team] = (wins_for_team + EPSILON) / (losses_for_team + EPSILON)

print initials

def win_likelihood(p1, p2):
	return (p1 * (1 - p2)) /
		(p1 * (1 - p2) + p2 * (1 - p1))
