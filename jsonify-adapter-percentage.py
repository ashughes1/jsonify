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

release_percents = process_json("https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=adapter_device_id&_facets_size=25&date=>%3D2015-05-18&release_channel=release")
beta_percents = process_json("https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=adapter_device_id&_facets_size=25&date=>%3D2015-05-18&release_channel=beta")
aurora_percents = process_json("https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=adapter_device_id&_facets_size=25&date=>%3D2015-05-18&release_channel=aurora")
nightly_percents = process_json("https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=adapter_device_id&_facets_size=25&date=>%3D2015-05-18&release_channel=nightly")

devices = []
for k in release_percents.keys():
    devices.append(k)

for k in beta_percents.keys():
    if k not in devices:
        devices.append(k)

for k in aurora_percents.keys():
    if k not in devices:
        devices.append(k)

for k in nightly_percents.keys():
    if k not in devices:
        devices.append(k)

string = '['
for d in devices:
    if d not in string:
        string += '{"device_id":"' + d + '",'

        if d in release_percents.keys():
            string += '"release":' + str(release_percents[d]) + ','
        else:
            string += '"release":' + str(float(0)) + ','

        if d in beta_percents.keys():
            string += '"beta":' + str(beta_percents[d]) + ','
        else:
            string += '"beta":' + str(float(0)) + ','

        if d in aurora_percents.keys():
            string += '"aurora":' + str(aurora_percents[d]) + ','
        else:
            string += '"aurora":' + str(float(0)) + ','

        if d in nightly_percents.keys():
            string += '"nightly":' + str(nightly_percents[d]) + '}'
        else:
            string += '"nightly":' + str(float(0)) + '}'

string += ']'
string = string.replace('}{', '},{')

f = open(filename, 'w')
f.write(string)
f.close()
