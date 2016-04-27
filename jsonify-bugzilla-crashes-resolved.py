import json
import os
import sys
import urllib2
import requests
from datetime import date
from datetime import timedelta

def get_total_from_json(url):
    data = requests.get(url).json()
    return len(data['bugs'])

def process_json(string):
    today = date.today()
    #total_reported = 2102 # Reported bugs between 2000-01-01 and 2014-03-31
    #total_resolved = 1627 # Resolved bugs between 2000-01-01 and 2014-03-31   
    domain = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id&product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'
    
    for i in range(90,1,-1):
        start_date = str(today-timedelta(days=i))
        end_date = str(today-timedelta(days=i))

        if start_date not in string:
            query_reported = domain + '&keywords=crash&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + start_date + '&chfieldto=' + end_date
            query_resolved = domain + '&keywords=crash&chfield=bug_status&chfieldvalue=RESOLVED&chfieldfrom=' + start_date + '&chfieldto=' + end_date
             #query_reported = domain + '&keywords=crash&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED'
            total_reported = get_total_from_json(query_reported)
            total_resolved = get_total_from_json(query_resolved)

            string += '{"date":"' + end_date + '","reported":' + str(total_reported) + ',"resolved":' + str(total_resolved) + '}'
        progress = int((float(90) - float(i)) / float(90) * 100)
        sys.stdout.write("Processing " + start_date + ": %d%% \r" % (progress) )
        sys.stdout.flush()

    return string

# def process_json(string):
#     today = date.today()
# 
#     for k in sorted(releases.keys(),reverse=True):
#         total = get_total_from_json('https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&f1=cf_status_firefox' + k[-2:] + '&o1=nowordssubstr&v1=---%2C+unaffected&f2=cf_status_firefox' + k[-2:] + '&o2=isnotempty&v2=&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + releases[k] + '&chfieldto=now')
#         string += '{"release":"' + k + '","total":' + total + '}'
#         sys.stdout.write("Processing data for " + k + '\n')
#         sys.stdout.flush()
# 
#     return string

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
    print string
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
