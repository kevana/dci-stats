'''Scrape finals scores from DCI.org and save as json.'''

from bs4 import BeautifulSoup
import json
from pprint import pprint
import requests
from datetime import datetime

# JSONify dates in ISO 8601 format
dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime)
    else json.JSONEncoder().default(obj))

allYearsEvents = {}
corps = []
params = {}

for year in range(1972, 2012):
    thisYear = {}
    params['year'] = year
    r = requests.get('http://www.dci.org/scores/archives/index.cfm', params=params)
    if r.status_code != 200:
        raise IOError('Unable to retrieve page for year %s' % year)
    soup = BeautifulSoup(r.text)
    scoresTable = soup.find_all('table')[2].\
                       find_all('table')[2].\
                       find_all('table')[2]

    infoHeader = soup.find_all('table')[2].\
                find_all('table')[2].\
                find('h3')
    cleanInfo = [item.strip() for item in infoHeader.text.split('\r\n') if item.strip()]

    # "Friday, August 18, 1972"
    thisYear['date'] = datetime.strptime(cleanInfo[0], '%A, %B %d, %Y')
    thisYear['city'] = cleanInfo[1].split(', ')[0]
    thisYear['state'] = cleanInfo[1].split(', ')[1]
    thisYear['name'] = cleanInfo[2]

    rows = scoresTable.findChildren('tr')[2:]  # First two rows are headers

    yearResultsList = []
    for row in rows:
        columns = row.findChildren('td')
        cleanColumns = [col.text.strip() for col in columns]

        result = {}
        result['place'] = cleanColumns[0]
        result['corps'] = cleanColumns[1]
        result['score'] = cleanColumns[2]
        yearResultsList.append(result)
        if cleanColumns[1] not in corps:
            corps.append(cleanColumns[1])

    thisYear['results'] = yearResultsList
    allYearsEvents[year] = [thisYear]
    print('Finished processing year %s' % year)

finalData = {'corps': corps,
            'events': allYearsEvents}

# Write all results to a file
with open('DCI-data.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, indent=2, default=dthandler))

with open('DCI-data-min.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, separators=(',', ':'), default=dthandler))
