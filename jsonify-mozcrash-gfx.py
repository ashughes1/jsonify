import httplib, json, os, requests, sys, time, urllib2
from datetime import date, datetime, timedelta

def get_json(url):
    try:
        json = requests.get(url).json()
    except:
        print('WARNING: No data for {} | Reattempting...').format(url)
        json = ''
    return json

def process_json(string):
    today = date.today()-timedelta(days=364)
    url = 'https://crash-stats.mozilla.com/api/SuperSearch/?moz_crash_reason=~GFX&date=%3E%3D' + str(today) + '&_histogram.date=adapter_vendor_id&_histogram_interval.date=1d'
    data = get_json(url)
    for d in data['facets']['histogram_date']:
        counts = {
            'amd':0,
            'intel':0,
            'nvidia':0
        }
        for c in d['facets']['adapter_vendor_id']:
            if c['term'] == '0x8086':
                counts['intel'] = c['count']
            elif c['term'] == '0x1002':
                counts['amd'] = c['count']
            elif c['term'] == '0x10de':
                counts['nvidia'] = c['count']
        string += '{"date":"' + d['term'][0:10] + '"' + ',"amd":' + str(counts['amd']) + ',"intel":' + str(counts['intel']) + ',"nvidia":' + str(counts['nvidia']) + ',"total":' + str(counts['amd']+counts['intel']+counts['nvidia']) + '}'
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    print process_json('')
    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #    string = process_json('')

    # string = string.replace('}{', '},{')
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
