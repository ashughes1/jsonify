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

def process_json():
    string = ""
    today = date.today()
    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            shutdown_count = get_total_from_json(start_date, 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers&shutdown_progress=shutdown&shutdown_progress=xpcom')
            total_count = get_total_from_json(start_date, 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&signature=~layers')
            shutdown_percent = int(float(shutdown_count)/float(total_count)*100)
            string += '{"date":"' + start_date + '","total":' + str(shutdown_percent) + '}'
            if i > 0:
                string += ','
        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Processing: %d%% \r" % (progress) )
        sys.stdout.flush()
    return '[' + string + ']'

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ""

    if os.path.exists(path):
        f = open(filename).read()
        # string = f.split('],[')

    f = open(filename, 'w')
    f.write(process_json())
    f.close()
