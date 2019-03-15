import json, sys, random, math
import numpy as np

teams = ["Arsenal", "Bournemouth", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Huddersfield", "Leicester", "Liverpool", "Man City", "Man United", "Newcastle", "Southampton", "Stoke", "Swansea", "Tottenham", "Watford", "West Brom", "West Ham"]
teamData = []

# Simulation Variables
numSeasons = 1000
searchTeam = False
searchTeamName = "Man City"

totalGoals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
totalPoints = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
highestGoals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
highestPoints = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lowestGoals = [100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
lowestPoints = [100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]

brightonWins = 0
palaceWins = 0

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
    generatedTeamData = []

    for team in teamData:
        generatedTeamData.append({"Name": team["Name"], "Wins": 0, "Draws": 0, "Losses": 0, "GoalsScored": 0, "HomeGoals": 0, "AwayGoals": 0,  "GoalsAgainst": 0, "GoalDifference": 0, "Points": 0})

    shuffledTeams = teams
    random.shuffle(shuffledTeams)

    for fixture in range(1, n):
        for i in range(n//2):
            matches.append((shuffledTeams[i], shuffledTeams[n - 1 - i]))
            random.shuffle(matches)
            return_matches.append((shuffledTeams[n - 1 - i], shuffledTeams[i]))
            random.shuffle(return_matches)
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

            if match[0] == "Brighton" and match[1] == "Crystal Palace":
                if homeFTGoals > awayFTGoals:
                     brightonWins += 1
                if awayFTGoals > homeFTGoals:
                    palaceWins += 1
                
            if match[0] == "Crystal Palace" and match[1] == "Brighton":
                if homeFTGoals > awayFTGoals:
                    palaceWins += 1
                if awayFTGoals > homeFTGoals:
                    brightonWins += 1

            for team in generatedTeamData:

                if match[0] == team["Name"]:
                    team["HomeGoals"] += homeFTGoals
                    team["GoalsScored"] += homeFTGoals
                    team["GoalsAgainst"] += awayFTGoals
                    team["GoalDifference"] += homeFTGoals - awayFTGoals
                    if homeFTGoals > awayFTGoals:
                        team["Wins"] += 1
                        team["Points"] += 3
                    if homeFTGoals == awayFTGoals:
                        team["Draws"] += 1
                        team["Points"] += 1
                    if homeFTGoals < awayFTGoals:
                        team["Losses"] += 1
                if match[1] == team["Name"]:
                    team["AwayGoals"] += awayFTGoals
                    team["GoalsScored"] += awayFTGoals
                    team["GoalsAgainst"] += homeFTGoals
                    team["GoalDifference"] += awayFTGoals - homeFTGoals
                    if awayFTGoals > homeFTGoals:
                        team["Wins"] += 1
                        team["Points"] += 3
                    if awayFTGoals == homeFTGoals:
                        team["Draws"] += 1
                        team["Points"] += 1
                    if awayFTGoals < homeFTGoals:
                        team["Losses"] += 1

            if searchTeam:
                if match[0] == searchTeamName or match[1] == searchTeamName:
                    print(match[0] + " " + str(homeFTGoals) + " - " + str(awayFTGoals) + " " + match[1])
            else:
                print(match[0] + " " + str(homeFTGoals) + " - " + str(awayFTGoals) + " " + match[1])
        print("------------------------------------------------------------")

    #Print League table at end of season
    print(" ")
    generatedTeamData.sort(reverse=True, key=lambda l: (l['Points'], l['GoalDifference'], l['GoalsScored']))
    dash = "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    print("League Table")
    print(dash)
    print('{:^10s}{:<18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}'.format("Pos", "Name", "Wins", "Draws", "Losses", "Goals Scored" ," Home Goals", "Away Goals", "Goals Against", "Goal Difference", "Points"))
    print(dash)
    currPos = 1
    for team in generatedTeamData:
        i = currPos-1
        totalGoals[i] += team["GoalsScored"]
        totalPoints[i] += team["Points"]
        if highestGoals[i] < team["GoalsScored"]:
            highestGoals[i] = team["GoalsScored"]
        if highestPoints[i] < team["Points"]:
            highestPoints[i] = team["Points"]
        if lowestGoals[i] > team["GoalsScored"]:
            lowestGoals[i] = team["GoalsScored"]
        if lowestPoints[i] > team["Points"]:
            lowestPoints[i] = team["Points"]
        #print(dash)
        print('{:^10d}{:<18s}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}'.format(currPos, team["Name"], team["Wins"], team["Draws"], team["Losses"], team["GoalsScored"], team["HomeGoals"], team["AwayGoals"], team["GoalsAgainst"], team["GoalDifference"], team["Points"]))
        currPos += 1
    print(dash)
    print(" ")

print("========================================================================================== Simulation Results ==========================================================================================")
print(" ")
print("Seasons simulated: " + str(numSeasons))
print("Total Goals Scored: " + str(sum(totalGoals)))
print("Brighton won " + str(brightonWins) + " times against Crystal Palace!")
print("")
print("--------------------------------------------------------------------------------------------------------------------------------")
print('{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}{:^18s}'.format("Pos", "Most Goals", "Least Goals", "Avg Goals", "Most Points", "Least Points", "Avg Points"))
print("--------------------------------------------------------------------------------------------------------------------------------")
for i in range(len(totalPoints)):
    currPos = i+1
    avgPoints = round(totalPoints[i]/numSeasons)
    avgGoals = round(totalGoals[i]/numSeasons)
    mostGoals = highestGoals[i]
    leastGoals = lowestGoals[i]
    mostPoints = highestPoints[i]
    leastPoints = lowestPoints[i]

    print('{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}{:^18d}'.format(currPos, mostGoals, leastGoals, avgGoals, mostPoints, leastPoints, avgPoints))
print("--------------------------------------------------------------------------------------------------------------------------------")
print("========================================================================================================================================================================================================")

