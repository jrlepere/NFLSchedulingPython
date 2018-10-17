
num_games_per_week = [16, 16, 16, 15, 15, 15, 14, 14, 13, 14, 13, 15, 16, 16, 16, 16, 16]
thanksgiving_gameslots = [161,162,163]
NUM_WEEKS = len(num_games_per_week)
london_games = [79, 94, 108]
mexico_games = [160]

# week gameslot matrix
week_gameslot = []
count = 0
for n in num_games_per_week:
	week_games = [0 for _ in range(256)]
	week_games[count:count+n] = [1 for _ in range(n)]
	count += n
	week_gameslot.append(week_games)
gameslot_week = np.array(week_gameslot, dtype=np.uint32).T
