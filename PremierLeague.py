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
    drawCount = 0
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
                    if homeGoals == awayGoals:
                        drawCount += 1
                    goalCount += homeGoals
                    homeGoalCount += homeGoals
                    homeGoalsConcededCount += awayGoals
                else:
                    if awayGoals > homeGoals:
                        awayWinCount += 1
                    if awayGoals == homeGoals:
                        drawCount += 1
                    goalCount += awayGoals
                    awayGoalCount += awayGoals
                    awayGoalsConcededCount += homeGoals

        # print(team + " scored " + str(goalCount) + " goals last season! (" + str(homeGoalCount) + " at home and " + str(awayGoalCount) + " away)")
        teamData.append({'Name': team , 'HomeGoals': homeGoalCount, 'AwayGoals': awayGoalCount , 'HomeConceded': homeGoalsConcededCount, 'AwayConceded': awayGoalsConcededCount , 'HomeWins': homeWinCount , 'AwayWins': awayWinCount , 'Draws': drawCount})

print("---------------------------------------")
for team in teamData:
    teamName = team["Name"]
    goalsFor = team["HomeGoals"] + team["AwayGoals"]
    goalsAgainst = team["HomeConceded"] + team["AwayConceded"]
    goalDifference = goalsFor - goalsAgainst
    goalsPerGame = goalsFor / 38
    points = (team["HomeWins"] * 3) + (team["AwayWins"]*3) + team["Draws"]
    pointsPerGame = points / 38

    print("Name: " + teamName)
    print("Goals For: " + str(goalsFor))
    print("Goals Against: " + str(goalsAgainst))
    print("Goal Difference: " + str(goalDifference))
    print("Goals Per Game: " + str(round(goalsPerGame,2)))
    print("Points: " + str(points))
    print("Points Per Game: " + str(round(pointsPerGame,2)))

    print("---------------------------------------")