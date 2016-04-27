import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

def get_total_from_json(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return str(len(data['bugs']))

def process_json(string):
    today = date.today()

    for i in range(110,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        week_date = str(today-timedelta(days=i+7))
        month_date = str(today-timedelta(days=i+30))

        if start_date not in string:
            total_day = get_total_from_json('https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&keywords=crash&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + start_date + '&chfieldto=' + end_date)
            total_week = get_total_from_json('https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&keywords=crash&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + week_date + '&chfieldto=' + end_date)
            total_month = get_total_from_json('https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&keywords=crash&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + month_date + '&chfieldto=' + end_date)

            resolved = get_total_from_json('https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&keywords=crash&chfield=bug_status&chfieldvalue=RESOLVED&chfieldfrom=' + start_date + '&chfieldto=' + end_date)

            string += '{"date":"' + start_date + '","total_day":' + total_day + ',"total_week":' + total_week + ',"total_month":' + total_month + '}'
        progress = int((float(365) - float(i)) / float(365) * 100)
        sys.stdout.write("Processing " + start_date + ": %d%% \r" % (progress) )
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
