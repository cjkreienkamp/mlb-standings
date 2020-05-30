# pr_01.py
# Description:
#   - if in season, display the score of the previous game and when it was for a team
#   - if in season, display the time and date of the next game for a team
#   - if in season, display the ranking of a team's division, wins, losses, and games back
#   - if out of season, display number of days until opening day (once it is less than 30)

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from datetime import datetime
import re
from tabulate import tabulate

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



# URL 1
#url1 = 'https://howmanydaysuntil.center/mlb-opening-day/'
#html1 = urllib.request.urlopen(url1, context=ctx).read()
#soup1 = BeautifulSoup(html1, 'html.parser')
#
#dayhour = soup1.find('span', class_='dhcountdown').text
#dayhour = dayhour.split()
#days = int(dayhour[0])
#hours = int(dayhour[2])
#if hours > 0:
#    days = days + 1
#print(days,'days until MLB opening day')



# URL 2
host2 = 'https://www.baseball-reference.com/boxes/?'
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day

url2 = host2 + f'month={month}&day={day}&year={year}'
try:
    html2 = urllib.request.urlopen(url2, context=ctx)
except:
    url2 = host2 + f'month=10&day=30&year=2019'
    html2 = urllib.request.urlopen(url2, context=ctx)
soup2 = BeautifulSoup(html2.read(), 'html.parser')

ALEast = ['NYY','TBR','BOS','TOR','BAL']
ALCentral = ['MIN','CLE','CHW','KCR','DET']
ALWest = ['HOU','OAK','TEX','LAA','SEA']
NLEast = ['ATL','WSN','NYM','PHI','MIA']
NLCentral = ['STL','MIL','CHC','CIN','PIT']
NLWest = ['LAD','ARI','SFG','COL','SDP']
teamInput = input('Input a 3 letter team name: ')
if teamInput in ALEast: division = 'AL East Division'
elif teamInput in ALCentral: division = 'AL Central Division'
elif teamInput in ALWest: division = 'AL West Division'
elif teamInput in NLEast: division = 'NL East Division'
elif teamInput in NLCentral: division = 'NL Central Division'
elif teamInput in NLWest: division = 'NL West Division'
else: 
    print('Invalid team name')
    quit()

for divisions in soup2.find_all('div', class_='table_wrapper'):
    if division == divisions.find('div', class_='section_heading').h2.text:
        attribute = divisions['id']
        break
    
mydata = list()
team = dict()
for teams in soup2.find( attrs = {'id':attribute} ).tbody.find_all('tr'):
    team['Team'] = teams.th.a.text
    team['W'] = teams.find( attrs = {'data-stat':'W'} ).text
    team['L'] = teams.find( attrs = {'data-stat':'L'} ).text
    team['W-L%'] = teams.find( attrs = {'data-stat':'win_loss_perc'} ).text
    team['GB'] = teams.find( attrs = {'data-stat':'games_back'} ).text
    mydata.append((team['Team'],team['W'],team['L'],team['W-L%'],team['GB']))

headers = ['Team','W','L','W-L%','GB']
print(tabulate(mydata, headers=headers))
