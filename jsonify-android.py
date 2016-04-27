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
    url = 'https://crash-stats.mozilla.com/api/SuperSearch/?product=FennecAndroid&signature=~gfx&signature=~layers&signature=~canvas&date=%3E%3D' + str(today) + '&_histogram.date=release_channel&_histogram_interval.date=1d'
    data = get_json(url)
    for d in data['facets']['histogram_date']:
        counts = {
            'release':0,
            'beta':0,
            'aurora':0,
            'nightly':0
        }
        for c in d['facets']['release_channel']:
            if c['term'] == 'release':
                counts['release'] = c['count']
            elif c['term'] == 'beta':
                counts['beta'] = c['count']
            elif c['term'] == 'aurora':
                counts['aurora'] = c['count']
            elif c['term'] == 'nightly':
                counts['nightly'] = c['count']
        string += '{"date":"' + d['term'][0:10] + '"' + ',"release":' + str(counts['release']) + ',"beta":' + str(counts['beta']) + ',"aurora":' + str(counts['aurora']) + ',"nightly":' + str(counts['nightly']) + '}'
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
