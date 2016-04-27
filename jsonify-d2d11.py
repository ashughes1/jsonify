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
    start_date = date.today()-timedelta(days=123)
    platforms = ['Windows XP',
                 'Windows Vista',
                 'Windows 7',
                 'Windows 8',
                 'Windows 10']
    
    result = {'?':{},'+':{},'-':{}}
    dates = []
    
    for key in result.keys():
        for platform in platforms:
            result[key][platform] = {}
            
            url = ""
            if key == '?':
                url = 'https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~D2D1.1%3F&date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform)
            elif key == '+':
                url = 'https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~D2D1.1%2B&date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform)
            elif key == '-':
                url = 'https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~D2D1.1-&date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform)
            
            if url != "":
                data = get_json(url)
                for d in data['facets']['histogram_date']:
                    result[key][platform][d['term'][0:10]] = d['facets']['cardinality_install_time']['value']
                    
                    found = 0
                    for i in range(len(dates)):
                        if d['term'][0:10] == dates[i]:
                            found = 1
                    if found != 1:
                        dates.append(d['term'][0:10])
    
    for d in sorted(dates):
        string += '{'
        string += '"date":"{:s}",'.format(d)
        for platform in platforms:
            attempt = 0
            success = 0
            fail = 0
        
            if result['?'].has_key(platform):
                if result['?'][platform].has_key(d):
                    attempt = result['?'][platform][d]
            if result['+'].has_key(platform):
                if result['+'][platform].has_key(d):
                    success = result['+'][platform][d]
            if result['-'].has_key(platform):
                if result['-'][platform].has_key(d):
                    fail = result['-'][platform][d]
            
            rate = float(0)
            if attempt != 0:
                rate = float(success)/float(attempt)*100
            string += '"{:s}":{:.2f},'.format(platform,rate)
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
