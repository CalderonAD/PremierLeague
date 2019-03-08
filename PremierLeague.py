import json
import sys

teams = ["Arsenal", "Bournemouth", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Huddersfield", "Leicester", "Liverpool", "Man City", "Man United", "Newcastle", "Southampton", "Stoke", "Swansea", "Tottenham", "Watford", "West Brom", "West Ham"]
teamData = []

print("Loading Data from JSON...")
# Load data from 17/18 season results
for team in teams:
    goalCount = 0
    homeGoalCount = 0
    awayGoalCount = 0
    homeWinCount = 0
    awayWinCount = 0
    homeGoalsConcededCount = 0
    awayGoalsConcededCount = 0
    with open('data/premierleague.json') as json_file:
        data = json.load(json_file)
        for match in data:

            homeTeam = match["HomeTeam"]
            awayTeam = match["AwayTeam"]
            homeGoals = match["FTHG"]
            awayGoals = match["FTAG"]

            if homeTeam == team or awayTeam == team:
                if homeTeam == team:
                    if homeGoals > awayGoals:
                        homeWinCount += 1
                    goalCount += homeGoals
                    homeGoalCount += homeGoals
                    homeGoalsConcededCount += awayGoals
                else:
                    if awayGoals > homeGoals:
                        awayWinCount += 1
                    goalCount += awayGoals
                    awayGoalCount += awayGoals
                    awayGoalsConcededCount += homeGoals

        # print(team + " scored " + str(goalCount) + " goals last season! (" + str(homeGoalCount) + " at home and " + str(awayGoalCount) + " away)")
        teamData.append({'Name': team , 'HomeGoals': homeGoalCount, 'AwayGoals': awayGoalCount , 'HomeConceded': homeGoalsConcededCount, 'AwayConceded': awayGoalsConcededCount , 'HomeWins': homeWinCount , 'AwayWins': awayWinCount})

for team in teamData:
    print(team)