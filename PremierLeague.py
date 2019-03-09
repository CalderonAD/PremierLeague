import json
import sys
import random
import math
import numpy as np

teams = ["Arsenal", "Bournemouth", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Huddersfield", "Leicester", "Liverpool", "Man City", "Man United", "Newcastle", "Southampton", "Stoke", "Swansea", "Tottenham", "Watford", "West Brom", "West Ham"]
teamData = []

# Simulation Variables
numSeasons = 1
searchTeam = True
searchTeamName = "Liverpool"

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

        avgHomeGoals = homeGoalCount/19
        avgAwayGoals = awayGoalCount/19
        avgHomeConceded = homeGoalsConcededCount/19
        avgAwayConceded = awayGoalsConcededCount/19
        # print(team + " scored " + str(goalCount) + " goals last season! (" + str(homeGoalCount) + " at home and " + str(awayGoalCount) + " away)")
        teamData.append({'Name': team , 'HomeGoals': homeGoalCount, 'AwayGoals': awayGoalCount , 'AverageHomeGoals': avgHomeGoals, 'AverageAwayGoals': avgAwayGoals, 'HomeConceded': homeGoalsConcededCount, 'AwayConceded': awayGoalsConcededCount , 'AverageHomeConceded': avgHomeConceded, 'AverageAwayConceded': avgAwayConceded, 'HomeWins': homeWinCount , 'AwayWins': awayWinCount})

overallAvgHomeGoals = 0
overallAvgAwayGoals = 0
totalAvgHomeGoals = 0
totalAvgAwayGoals = 0
overallAvgHomeConceded = 0
overallAvgAwayConceded = 0
totalAvgHomeConceded = 0
totalAvgAwayConceded = 0
for team in teamData:
    totalAvgHomeGoals += team["AverageHomeGoals"]
    totalAvgAwayGoals += team["AverageAwayGoals"]
    totalAvgHomeConceded += team["AverageHomeConceded"]
    totalAvgAwayConceded += team["AverageAwayConceded"]

overallAvgHomeGoals = totalAvgHomeGoals / len(teams)
overallAvgAwayGoals = totalAvgAwayGoals / len(teams)
overallAvgHomeConceded = totalAvgHomeConceded / len(teams)
overallAvgAwayConceded = totalAvgAwayConceded / len(teams)

print("------------------------------------------------------------")
for i in range(numSeasons):
    print("--- Season " + str(i+1) + " ---")
    #Generate Random fixture list
    n = len(teams)
    matches = []
    fixtures = []
    return_matches = []

    shuffledTeams = teams
    random.shuffle(shuffledTeams)

    for fixture in range(1, n):
        for i in range(n//2):
            matches.append((shuffledTeams[i], shuffledTeams[n - 1 - i]))
            return_matches.append((shuffledTeams[n - 1 - i], shuffledTeams[i]))
        teams.insert(1, shuffledTeams.pop())
        fixtures.insert(len(fixtures)//2, matches)
        fixtures.append(return_matches)
        matches = []
        return_matches = []

    matchDay = 1
    print("------------------------------------------------------------")
    # Work out results based on poisson distribution
    for fixture in fixtures:
        print("Matchday " + str(matchDay) + ":")
        matchDay += 1
        for match in fixture:
            homeTeamAttackStrength = 0
            homeTeamDefenseStrength = 0
            awayTeamAttackStrength = 0
            awayTeamDefenseStrength = 0
            homeFTGoals = 0
            awayFTGoals = 0
            for team in teamData:
                #Home Team
                if team["Name"] == match[0]:
                    homeTeamAttackStrength = team["AverageHomeGoals"] / overallAvgHomeGoals
                    homeTeamDefenseStrength = team["AverageHomeConceded"] / overallAvgHomeConceded
                if team["Name"] == match[1]:
                    awayTeamAttackStrength = team["AverageAwayGoals"] / overallAvgAwayGoals
                    awayTeamDefenseStrength = team["AverageAwayConceded"] / overallAvgAwayConceded

            homeLambda = overallAvgHomeGoals * homeTeamAttackStrength * awayTeamDefenseStrength
            awayLambda = overallAvgAwayGoals * awayTeamAttackStrength * homeTeamDefenseStrength

            homeFTGoals = np.random.poisson(homeLambda)
            awayFTGoals = np.random.poisson(awayLambda)
            if searchTeam:
                if match[0] == searchTeamName or match[1] == searchTeamName:
                    print(match[0] + " " + str(homeFTGoals) + " - " + str(awayFTGoals) + " " + match[1])
            else:
                print(match[0] + " " + str(homeFTGoals) + " - " + str(awayFTGoals) + " " + match[1])
        print("------------------------------------------------------------")
