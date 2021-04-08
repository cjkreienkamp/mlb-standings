import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
#import ssl
#from datetime import datetime
#import re
#from tabulate import tabulate

# Ignore SSL certificate errors
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

def division():
    host2 = 'https://www.baseball-reference.com/boxes/?'
    year = 2020#datetime.today().year
    month = 6#datetime.today().month
    day = 24#datetime.today().day

    url2 = host2 + f'month={month}&day={day}&year={year}'
    try:
        html2 = urllib.request.urlopen(url2, context=ctx)
    except:
        url2 = host2 + f'month=10&day=30&year=2019'
        html2 = urllib.request.urlopen(url2)
    soup2 = BeautifulSoup(html2.read(), 'html.parser')
      
    ALEast = ['NYY','TBR','BOS','TOR','BAL']
    ALCentral = ['MIN','CLE','CHW','KCR','DET']
    ALWest = ['HOU','OAK','TEX','LAA','SEA']
    NLEast = ['ATL','WSN','NYM','PHI','MIA']
    NLCentral = ['STL','MIL','CHC','CIN','PIT']
    NLWest = ['LAD','ARI','SFG','COL','SDP']
    #teamInput = input('Input a 3 letter team name: ')
    teamInput = 'STL'
    if teamInput in ALEast: division = 'AL East Division'
    elif teamInput in ALCentral: division = 'AL Central Division'
    elif teamInput in ALWest: division = 'AL West Division'
    elif teamInput in NLEast: division = 'NL East Division'
    elif teamInput in NLCentral: division = 'NL Central Division'
    elif teamInput in NLWest: division = 'NL West Division'
        
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

    return mydata

def speak():
    url = 'https://howmanydaysuntil.center/mlb-opening-day/'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    dayhour = soup.find('span', class_='dhcountdown').text
    dayhour = dayhour.split()
    days = int(dayhour[0])
    hours = int(dayhour[2])
    if hours > 0:
        days = days + 1
        days = 0 # TAKE THIS OUT AFTER TWEAKING
    if days > 0: output = f'There are {days} days until MLB opening day'
    else:
        data = division()
        count = 0
        while count < 5:
            if data[count][0] == 'STL':
                index = count
            count = count + 1
        if (index == 0 or index == 1) and (data[1][4] == '--'): # tied for first
            if index == 0: team_of_interest = data[1][0]
            elif index == 1: team_of_interest = data[0][0]
            if team_of_interest == 'STL': team_of_interest = 'St. Louis Cardinals'
            elif team_of_interest == 'MIL': team_of_interest = 'Milwaukee Brewers'
            elif team_of_interest == 'CHC': team_of_interest = 'Chicago Cubs'
            elif team_of_interest == 'CIN': team_of_interest = 'Cincinnati Reds'
            elif team_of_interest == 'PIT': team_of_interest = 'Pittsburgh Pirates'
            output = f'The Cardinals are tied for first place with the {team_of_interest}.'
        elif index == 0: # the Cardinals are in first place
            team_of_interest = data[1][0]
            second_place_gb = data[1][4]
            if team_of_interest == 'STL': team_of_interest = 'St. Louis Cardinals'
            elif team_of_interest == 'MIL': team_of_interest = 'Milwaukee Brewers'
            elif team_of_interest == 'CHC': team_of_interest = 'Chicago Cubs'
            elif team_of_interest == 'CIN': team_of_interest = 'Cincinnati Reds'
            elif team_of_interest == 'PIT': team_of_interest = 'Pittsburgh Pirates'
            output = f'The Cardinals are in first place. They are {second_place_gb} games ahead of the {team_of_interest}.'
        else:    
            team_of_interest = data[0][0]
            gamesback = data[index][4]
            if team_of_interest == 'STL': team_of_interest = 'St. Louis Cardinals'
            elif team_of_interest == 'MIL': team_of_interest = 'Milwaukee Brewers'
            elif team_of_interest == 'CHC': team_of_interest = 'Chicago Cubs'
            elif team_of_interest == 'CIN': team_of_interest = 'Cincinnati Reds'
            elif team_of_interest == 'PIT': team_of_interest = 'Pittsburgh Pirates'
            if index == 1: # the Cardinals are in second place
                output = f'The Cardinals are in second place. They are {gamesback} games behind the {team_of_interest}.'
            elif index == 2: # the Cardinals are in third place
                output = f'The Cardinals are in third place. They are {gamesback} games behind the {team_of_interest}.'
            elif index == 3: # the Cardinals are in fourth place
                output = f'The Cardinals are in fourth place. They are {gamesback} games behind the {team_of_interest}.'
            elif index == 4: # the Cardinals are in last place
                output = f'The Cardinals are in last place. They are {gamesback} games behind the {team_of_interest}.'

    return output
    
    
    
    
    
    
    
    
    
    
    
    
    