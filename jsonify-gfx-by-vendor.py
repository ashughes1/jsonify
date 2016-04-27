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
    out = '{"date":"' + start_date + '","total":' + total + '}'
    return out

def process_json(string, vendor):
    today = date.today()
    
    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            query = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~gfx&adapter_vendor_id=' + vendor
            string += ',' + get_total_from_json(start_date, query)
        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Processing " + vendor + ": %d%% \r" % (progress) )
        sys.stdout.flush()
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ['[]','[]','[]']
    
    if os.path.exists(path):
        f = open(filename).read()
        string = f.split('],[')
    
    f = open(filename, 'w')
    f.write('[')
        
    for i in range(0, len(string)):
        if i == 0:
            f.write('[' + process_json(string[i].strip('[]'), '0x1002') + '],')
        elif i == 1:
            f.write('[' + process_json(string[i].strip('[]'), '0x8086') + '],')
        elif i == 2:
            f.write('[' + process_json(string[i].strip('[]'), '0x10de') + ']')
    
    f.write(']')
    f.close()

