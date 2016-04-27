import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

def get_total_from_json(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    channels = data['facets'][u'release_channel']
    counts = {'nightly':0,'aurora':0,'beta':0,'release':0}
    for i in range(0, len(channels)):
        if counts.has_key(channels[i]['term']):
            counts[channels[i]['term']] = channels[i]['count']
    return counts

def process_json(string):
    today = date.today()

    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            url = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~nvwgf2um.dll&signature=~nvumdshim.dll&signature=~nvapi.dll&signature=~nvd3dum.dll&signature=~nvlsp.dll&signature=~nvlsp64.dll&_facets=release_channel'
            totals = get_total_from_json(url)
            string += '{"date":"' + start_date + '",'
            string += '"nightly":' + str(totals['nightly']) + ','
            string += '"aurora":' + str(totals['aurora']) + ','
            string += '"beta":' + str(totals['beta']) + ','
            string += '"release":' + str(totals['release']) + '}'
        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Progress: %d%% \r" % (progress) )
        sys.stdout.flush()
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ''
    if os.path.exists(path):
        f = open(filename).read()
        string = process_json(f.strip('[]'))
    else:
        string = process_json('')

    string = string.replace('}{', '},{')
    f = open(filename, 'w')
    f.write('[' + string + ']')
    f.close()
