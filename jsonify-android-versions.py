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
    data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?product=FennecAndroid&release_channel=release&release_channel=beta&date=%3E%3D' + str(today) + '&_facets=android_version&_facets_size=5')
    versions = ''
    counts = {}
    for d in data['facets']['android_version']:
        counts[d['term'][0:2]] = 0
        versions += '&android_version=~{0}'.format(d['term'][0:2])
    data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?product=FennecAndroid&release_channel=release&release_channel=beta' + versions + '&date=%3E%3D' + str(today) + '&_histogram.date=android_version&_histogram_interval.date=1d')
    for d in data['facets']['histogram_date']:
        string += '{"date":"' + d['term'][0:10] + '"'
        for a in d['facets']['android_version']:
            if a['term'][0:2] in counts:
                counts[a['term'][0:2]] += a['count']
        for k in counts.keys():
            string += ',"{0}":{1:d}'.format(k, counts[k])
            counts[k] = 0
        string += '}'
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    print string
    return string






if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    #print process_json('')
    process_json('')
    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #    string = process_json('')

    # string = string.replace('}{', '},{')
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
