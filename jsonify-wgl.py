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
    start_date = date.today()-timedelta(days=223)
    platforms = ['Windows XP',
                 'Windows Vista',
                 'Windows 7',
                 'Windows 8',
                 'Windows 10']
    
    crashes = {}
    percents = {}
    dates = []
    
    for platform in platforms:
        crashes[platform] = {}
        percents[platform] = {}
        wgl_data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~WGL%2B&date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform))
        all_data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform))
        
        for d in wgl_data['facets']['histogram_date']:
            crashes[platform][d['term'][0:10]] = d['facets']['cardinality_install_time']['value']
            found = 0
            for i in range(len(dates)):
                if d['term'][0:10] == dates[i]:
                    found = 1
            if found != 1:
                dates.append(d['term'][0:10])
        for d in all_data['facets']['histogram_date']:
            if crashes[platform].has_key(d['term'][0:10]):
                percents[platform][d['term'][0:10]] = float(crashes[platform][d['term'][0:10]])/float(d['facets']['cardinality_install_time']['value'])*100
                
    string += '{"crashes":['
    for d in sorted(dates):
        string += '{'
        string += '"date":"{:s}",'.format(d)
        for platform in platforms:
            if crashes[platform].has_key(d):
                string += '"{:s}":{:d},'.format(platform,crashes[platform][d])
            else:
                string += '"{:s}":{:d},'.format(platform,0)
        string += '}'
    string += '],"percents":['
    for d in sorted(dates):
        string += '{'
        string += '"date":"{:s}",'.format(d)
        for platform in platforms:
            if crashes[platform].has_key(d):
                string += '"{:s}":{:.2f},'.format(platform,percents[platform][d])
            else:
                string += '"{:s}":{:.2f},'.format(platform,0)
        string += '}'
    string += ']}'
    
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
