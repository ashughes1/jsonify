import json
import os
import sys
import urllib2
from datetime import date, datetime, timedelta


BUGZILLA_SERVER = 'bugzilla.mozilla.org'
BUGZILLA_REST_URL = 'https://{}/rest/bug?'.format(BUGZILLA_SERVER)
BUGZILLA_PRODUCT_LIST = 'product=Core'
BUGZILLA_COMPONENT_LIST = '&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'

def get_json(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

def process_json(string):
    today = date.today()
    domain = BUGZILLA_REST_URL + BUGZILLA_PRODUCT_LIST + BUGZILLA_COMPONENT_LIST

    for i in range(2015,2017,1):
        query = domain + '&resolution=FIXED&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom={}-01-01&chfieldto={}-12-31'.format(str(i), str(i))
        query += '&include_fields=id,summary,status,cf_last_resolved,creation_time'
        data = get_json(query)

        if len(data['bugs']) > 0:
            time_to_fix_total = timedelta()
            time_to_fix_average = 0

            for b in data['bugs']:
                if not b['cf_last_resolved'] == None:
                    date_resolved = datetime.strptime(b['cf_last_resolved'], '%Y-%m-%dT%H:%M:%SZ')
                    date_created = datetime.strptime(b['creation_time'], '%Y-%m-%dT%H:%M:%SZ')
                    time_difference = date_resolved - date_created
                    time_to_fix_total += time_difference

            time_to_fix_average = time_to_fix_total / len(data['bugs'])
            string += '{"date":"' + str(i) + '","days_total":' + str(time_to_fix_total.days) + ',"days_avg":' + str(time_to_fix_average.days) + '}'
        else:
            string += '{"date":"' + str(i) + '","days_total":0,"days_avg":0}'

        print 'Processed data for ' + str(i)

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
