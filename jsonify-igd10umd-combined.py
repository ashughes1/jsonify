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
    start_date = date.today()-timedelta(days=363)
    data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?&signature=~igd10umd&date=%3E%3D{:s}&_histogram.date=release_channel&histogram_interval=1d'.format(str(start_date)))
    
    for d in data['facets']['histogram_date']:
        string += '{'
        string += '"date":"{:s}"'.format(d['term'][0:10])
        for channel in d['facets']['release_channel']:
            if channel['term'] == 'nightly' or channel['term'] == 'aurora' or channel['term'] == 'beta' or channel['term'] == 'release':
                string += ',"{:s}":{:d}'.format(channel['term'],channel['count'])
        string += '}'

    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ""

    print process_json('')

    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #     string = process_json('')

    # f = open(filename, 'w')
    # f.write('[' + process_json(string) + ']')
    # f.close()
