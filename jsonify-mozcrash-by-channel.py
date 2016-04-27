import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

def get_total_from_json(start_date, url):
    response = urllib2.urlopen(url)
    json_get = response.read()
    pos_total = json_get.find('"total":')
    pos_facets = json_get.find('"facets":')
    total = json_get[pos_total+9:pos_facets-3]
    return total

def process_json(s):
    today = date.today()
    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        url = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&moz_crash_reason=%3DMOZ_CRASH(GFX_CRASH)'
        if start_date not in s:
            nightly = get_total_from_json(start_date, url + '&release_channel=nightly')
            aurora = get_total_from_json(start_date, url + '&release_channel=aurora')
            beta = get_total_from_json(start_date, url + '&release_channel=beta')
            release = get_total_from_json(start_date, url + '&release_channel=release')
            s += '{"date":"' + start_date + '","nightly":' + str(nightly) + ',"aurora":' + str(aurora) + ',"beta":' + str(beta) + ',"release":' + str(release) + '}'
        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Processing: %d%% \r" % (progress) )
        sys.stdout.flush()
    return s

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
