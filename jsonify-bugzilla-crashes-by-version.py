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

    domain = 'https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'

    for i in range(48,43,-1):
        query_reported = domain + '&keywords=crash&f1=cf_status_firefox' + str(i) + '&o1=nowordssubstr&v1=---%2C+unaffected&f2=cf_status_firefox' + str(i) + '&o2=isnotempty&v2='
        query_resolved = domain + '&keywords=crash&f1=cf_status_firefox' + str(i) + '&o1=anywordssubstr&v1=fixed%2C+verified%2C+disabled&f2=cf_status_firefox' + str(i) + '&o2=isnotempty&v2='
        total_reported = get_total_from_json(query_reported)
        total_resolved = get_total_from_json(query_resolved)
        print '{"release":"Firefox ' + str(i) + '","reported":' + total_reported + ',"resolved":' + total_resolved + '}'
        string += '{"release":"Firefox ' + str(i) + '","reported":' + total_reported + ',"resolved":' + total_resolved + '}'
        sys.stdout.write("Processing data for Firefox " + str(i) + " / 42\n")
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
    print '[' + string + ']'
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
