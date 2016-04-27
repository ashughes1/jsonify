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
        url = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&adapter_vendor_id=0x8086&adapter_device_id=0x0046'
        if start_date not in s:
            driver_count = get_total_from_json(start_date, url + '&adapter_driver_version=8.15.10.2086')
            device_count = get_total_from_json(start_date, url)
            driver_percent = int(float(driver_count)/float(device_count)*100)
            s += '{"date":"' + start_date + '","driver_count":' + str(driver_count) + ',"device_count":' + str(device_count) + ',"driver_percent":' + str(driver_percent) + '}'
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
