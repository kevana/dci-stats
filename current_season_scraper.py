'''
Score scraper for the current DCI season.
'''

from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
from time import sleep

# Enter the current year of competition as a string
year = '2013'

allYearsEvents = {year: []}
corps = []
locations = []
params = {}

# JSONify dates in ISO 8601 format
dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime)
    else json.JSONEncoder().default(obj))

# URL redirects to the most recent score data
r = requests.get('http://www.dci.org/scores', allow_redirects=True)
if r.status_code != 200:
    raise IOError('Unable to load dci.org/scores')
soup = BeautifulSoup(r.text)
options = soup.find('select').findChildren()
event_ids = [opt['value'] for opt in options]

for idx in event_ids:
    thisEvent = {}
    params = {'event': idx}
    r = requests.get('http://www.dci.org/scores/index.cfm', params=params)
    soup = BeautifulSoup(r.text)

    scoresTable = (soup.find_all('table')[5].
                   find_all('table')[1])

    infoHeader = (soup.find_all('table')[5].
                  find('h3'))
    infoList = list(infoHeader.strings)

    thisEvent['date'] = datetime.strptime(infoList[0], '%A, %B %d, %Y')
    thisEvent['name'] = infoList[2]

    loc = infoList[1].rsplit(' ', 1)
    thisEvent['city'] = loc[0].rstrip(',\n\r\t ')
    thisEvent['state'] = loc[1]

    if infoList[1] not in locations:
        locations.append(infoList[1])

    # First two rows are headers, last is recap
    rows = scoresTable.findChildren('tr')[2:-2]

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

    thisEvent['results'] = yearResultsList
    allYearsEvents[year].append(thisEvent)
    print('Finished processing event: %s' % thisEvent['name'])
    sleep(1)  # Don't DOS the DCI website

finalData = {'corps': corps.sorted(),
             'events': allYearsEvents,
             'locations': locations}

# Write all results to a file
with open('DCI-2013-season.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, indent=2, default=dthandler))

with open('DCI-2013-season.min.json', 'w') as outFile:
    outFile.write(json.dumps(finalData, sort_keys=True, separators=(',', ':'), default=dthandler))
