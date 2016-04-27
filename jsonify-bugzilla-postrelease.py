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
    releases = {'Firefox 10':'2012-01-31',
                'Firefox 11':'2012-03-13',
                'Firefox 12':'2012-04-24',
                'Firefox 13':'2012-06-05',
                'Firefox 14':'2012-07-17',
                'Firefox 15':'2012-08-28',
                'Firefox 16':'2012-10-09',
                'Firefox 17':'2012-11-20',
                'Firefox 18':'2013-01-08',
                'Firefox 19':'2013-02-19',
                'Firefox 20':'2013-04-02',
                'Firefox 21':'2013-05-14',
                'Firefox 22':'2013-06-25',
                'Firefox 23':'2013-08-06',
                'Firefox 24':'2013-09-17',
                'Firefox 25':'2013-10-29',
                'Firefox 26':'2013-12-10',
                'Firefox 27':'2014-02-04',
                'Firefox 28':'2014-03-18',
                'Firefox 29':'2014-04-29',
                'Firefox 30':'2014-06-10',
                'Firefox 31':'2014-07-22',
                'Firefox 32':'2014-09-02',
                'Firefox 33':'2014-10-14',
                'Firefox 34':'2014-12-01',
                'Firefox 35':'2015-01-13',
                'Firefox 36':'2015-02-24',
                'Firefox 37':'2015-03-31',
                'Firefox 38':'2015-05-12',
                'Firefox 39':'2015-06-30',
                'Firefox 40':'2015-08-11',
                'Firefox 41':'2015-09-22',
                'Firefox 42':'2015-11-03',
                'Firefox 43':'2015-12-15',
                'Firefox 44':'2016-01-26',
                'Firefox 45':'2016-03-08'}

    for k in sorted(releases.keys(),reverse=True):
        query_reported = domain + '&f1=cf_status_firefox' + k[-2:] + '&o1=nowordssubstr&v1=---%2C+unaffected&f2=cf_status_firefox' + k[-2:] + '&o2=isnotempty&v2=&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + releases[k] + '&chfieldto=now'
        query_resolved = domain + '&f1=cf_status_firefox' + k[-2:] + '&o1=anywordssubstr&v1=fixed%2C+verified%2C+disabled&f2=cf_status_firefox' + k[-2:] + '&o2=isnotempty&v2=&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + releases[k] + '&chfieldto=now'
        total_reported = get_total_from_json(query_reported)
        total_resolved = get_total_from_json(query_resolved)

        string += '{"release":"' + k + '","reported":' + total_reported + ',"resolved":' + total_resolved + '}'
        sys.stdout.write("Processing data for " + k + '\n')
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
    string = '[' + string + ']'
    print string
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
