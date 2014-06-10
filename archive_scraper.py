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
locations = []
params = {}

for year in range(1972, 2012):
    thisYear = {}
    params['year'] = year
    r = requests.get('http://www.dci.org/scores/archives/index.cfm',
                     params=params)
    if r.status_code != 200:
        raise IOError('Unable to retrieve page for year %s' % year)
    soup = BeautifulSoup(r.text)
    scoresTable = (soup.find_all('table')[2].
                   find_all('table')[2].
                   find_all('table')[2])

    infoHeader = (soup.find_all('table')[2].
                  find_all('table')[2].
                  find('h3'))
    infoList = [item.strip() for item in list(infoHeader.strings)]

    thisYear['date'] = datetime.strptime(infoList[0], '%A, %B %d, %Y')
    thisYear['name'] = infoList[2]

    loc = infoList[1].rsplit(' ', 1)
    thisYear['city'] = loc[0].rstrip(',\n\r\t ')
    thisYear['state'] = loc[1]

    if infoList[1] not in locations:
        locations.append(infoList[1])

    # First two rows are headers
    rows = scoresTable.findChildren('tr')[2:]
    yearResultsList = []
    for row in rows:
        columns = row.findChildren('td')
        cleanColumns = [col.text.strip() for col in columns]

        if len(cleanColumns) < 3:
            break  # Some events have Exhibition/International class labels

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
             'events': allYearsEvents,
             'locations': locations}

# Write all results to a file
with open('DCI-finals-1972-2011.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, indent=2, default=dthandler))

with open('DCI-finals-1972-2011.min.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, separators=(',', ':'), default=dthandler))
