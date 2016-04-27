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
                 'Windows 10',
                 'OS X',
                 'Linux']
    
    result = {}
    for platform in platforms:
        result[platform] = {}
        data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?&signature=~gfx&signature=~layers&signature=~canvas&date=%3E%3D{:s}&platform_pretty_version=~{:s}&_histogram.date=_cardinality.install_time&_histogram_interval=1d'.format(str(start_date),platform))
        for d in data['facets']['histogram_date']:       
            crashes = d['count']
            installs = d['facets']['cardinality_install_time']['value']
            rate = float(crashes)/float(installs)
            result[platform][d['term'][0:10]] = rate
    
    dates = []
    for platform in result.keys():
        for d in result[platform].keys():
            found = 0
            for i in range(len(dates)):
                if d == dates[i]:
                    found = 1
            if found == 0:
                dates.append(d)    
    dates = sorted(dates)
    
    for i in range(len(dates)):
        string += '{'
        string += '"date":"{:s}",'.format(dates[i])
        for platform in result.keys():
            if result[platform].has_key(dates[i]):
                string += '"{:s}":{:.2f},'.format(platform,result[platform][dates[i]])
            else:
                string += '"{:s}":0,'.format(platform,result[platform][dates[i]])
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
