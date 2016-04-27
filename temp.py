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
    result = []
    data = requests.get('https://crash-stats.mozilla.com/api/SuperSearch/?&signature=~compute_image_info&date=%3E%3D2015-04-29&date=%3C%3D2016-04-26&_histogram.date=release_channel&_histogram_interval=1d').json()
    for facet_date in data['facets']['histogram_date']:
        result.append({'date':str(facet_date['term'][0:10]),'count':facet_date['count']})
    string = str(result);
    string = string.replace('\'', '"')
    string = string.replace(' ', '')
    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
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
