import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

URL_CRASH_STATS = 'https://crash-stats.mozilla.com/api/SuperSearch/?'
MAX_DATE_RANGE = 180

def get_total_from_json(start_date, url):
    response = urllib2.urlopen(url)
    json_get = response.read()
    pos_total = json_get.find('"total":')
    pos_facets = json_get.find('"facets":')
    total = json_get[pos_total+9:pos_facets-3]
    return total

def process_json(s, max_date_range=MAX_DATE_RANGE):
    today = date.today()

    for i in range(max_date_range,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in s:
            #url_uptime = URL_CRASH_STATS + 'date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers&uptime=<%3D8'
            url_uptime = '{0}date=%3E%3D{1}&date=%3C{2}&signature=~gfx&signature=~layers&uptime=<%3D8'.format(URL_CRASH_STATS, start_date, end_date)
            #startup_count = get_total_from_json(start_date, URL_CRASH_STATS + 'date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers&uptime=<%3D8')
            startup_count = get_total_from_json(start_date, url_uptime)
            shutdown_count = get_total_from_json(start_date, URL_CRASH_STATS + 'date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers&shutdown_progress=shutdown&shutdown_progress=xpcom')
            total_count = get_total_from_json(start_date, URL_CRASH_STATS + 'date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers')
            startup_percent = int(float(startup_count)/float(total_count)*100)
            shutdown_percent = int(float(shutdown_count)/float(total_count)*100)
            other_percent = 100 - startup_percent - shutdown_percent
            s += '{"date":"' + start_date + '","startup":' + str(startup_percent) + ',"shutdown":' + str(shutdown_percent) + ',"other":' + str(other_percent) + '}'

        progress = int((float(max_date_range) - float(i)) / float(max_date_range) * 100)
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
        string = process_json(f.strip('[]'), 1)
    else:
        string = process_json('', 1)

    string = string.replace('}{', '},{')
    f = open(filename, 'w')
    f.write('[' + string + ']')
    f.close()
