import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

def get_total_from_json(url):
    response = urllib2.urlopen(url)
    json_get = response.read()
    pos_total = json_get.find('"total":')
    pos_facets = json_get.find('"facets":')
    total = json_get[pos_total+9:pos_facets-3]
    return total

def process_json(url):
    data = {}
    total = get_total_from_json(url)
    response = urllib2.urlopen(url)
    json_get = response.read()
    pos_adapters = json_get.find('adapter_device_id')
    items = json_get[pos_adapters+22:].split('{')

    for item in items:
        item = item.replace('\n', '')
        item = item.replace('},', '')
        item = item.replace('}]}}', '')

        i = item.split(',')
        if len(i) == 2:
            device_id = i[1].strip()[9:-1]
            count = i[0].strip()[9:]
            if count != '':
                data[device_id] = float(count)/float(total)*100
    return data


if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename

#    if os.path.exists(path):
#        f = open(filename).read()
vendors = ['0x1002','0x8086','0x10de']
url_root = "https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=adapter_device_id&_facets_size=25&date=>%3D2015-05-18"
channels = ['release','beta','aurora','nightly']
string = ""

# Get the initial data from Socorro
string += '['
for vendor in vendors:
    string += '['
    vendor_data = []
    devices = []
    for channel in channels:
        # Retreive the json from Socorro for (vendor) and (channel)
        json = process_json(url_root + '&release_channel=' + channel + '&adapter_vendor_id=' + vendor)

        # Catalog all devices
        for k in json.keys():
            if k not in devices:
                devices.append(k)
        vendor_data.append(json)

    for d in devices:
        values = [float(0), float(0), float(0), float(0)]
        for i in range(0, len(vendor_data)):
            if d in vendor_data[i].keys():
                values[i] = vendor_data[i][d]
        string += '{"device_id":"' + d + '","release":' + str(values[0]) + ',"beta":' + str(values[1]) + ',"aurora":' + str(values[2]) + ',"nightly":' + str(values[3]) + '}'

    string += ']'

string += ']'
string = string.replace('}{', '},{')
string = string.replace('][', '],[')

f = open(filename, 'w')
f.write(string)
f.close()
