 
import http.client
import json
import time
import datetime


def compareScores(home, hScore, visitor, vScore):
  if(hScore > vScore):
    print('The %s beat the %s' % (home,visitor))
    print('The final score was: %s - %s' % (hScore,vScore))
  else:
    print('The %s beat the %s' % (visitor,home))
    print('The final score was: %s - %s' % (vScore,hScore))


conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
    'x-rapidapi-key': "bec9166da9mshc65825fc4dddf78p19c1e6jsn30feec0b19e6"
    }

conn.request("GET", "/games/live/", headers=headers)

res = conn.getresponse()
data = res.read()

d = json.loads(data)

games = d['api']['games']
if not games:
  #There are no live games so find the last played Bulls game
  conn.request("GET", "/games/teamId/6", headers=headers)
  res = conn.getresponse()
  data = res.read()
  d = json.loads(data)
  games = d['api']['games']
  for game in games[400:]:
    if game['endTimeUTC'] == '':
      break
    mostRecentGame = game
  visitor = mostRecentGame['vTeam']['nickName']
  vScore = mostRecentGame['vTeam']['score']['points']
  home = mostRecentGame['hTeam']['nickName']
  hScore = mostRecentGame['hTeam']['score']['points']
  compareScores(home, hScore, visitor, vScore)

else:
  #There are live games
  for i in range(len(games)):
    print('game %d: ' % i)
    visitor = d['api']['games'][i]['vTeam']['nickName']
    home = games[i]['hTeam']['nickName']
    vScore = games[i]['vTeam']['score']['points']
    hScore = games[i]['hTeam']['score']['points']
    clock = games[i]['clock']
    quarter = games[i]['currentPeriod']
    endTime = games[i]['endTimeUTC']
    startTime = games[i]['startTimeUTC']

    if(clock != ''):
      if(quarter == '0'):
        print('The game has not started yet')
      elif (quarter == '1'):
        print('%s %sst' % (clock,quarter))
      elif(quarter == '2'):
        print('%s %snd' % (clock,quarter))
      elif(quarter == '3'):
        print('%s %srd' % (clock,quarter))
      elif(quarter == '4'):
        print('%s %sth' % (clock,quarter))
      else:
        print('uhhhhhhhh')
      print('%s: %s' % (home, hScore))
      print('%s: %s' % (visitor, vScore))
      print()
    elif endTime != '':
      print('The game is over!')
      compareScores(home, int(hScore), visitor, int(vScore))
      print()
    
    else:
      print('This game has not started yet')
      print('%s vs %s' % (home,visitor))
      print('The game will start at %s')
      print()
