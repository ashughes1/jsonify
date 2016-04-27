import httplib, json, os, requests, sys, time, urllib2
from datetime import date, datetime, timedelta

def get_json(url):
    try:
        json = requests.get(url).json()
    except:
        print('WARNING: No data for {} | Reattempting...').format(url)
        json = get_json(url)
    return json

def process_json(string):
    data = json.loads(string)

    s = ''
    amd = data[0]
    intel = data[1]
    nvidia = data[2]

    for i in range(0, len(amd)):
        s += '{"date":"' + str(amd[i]['date']) + '",'
        s += '"amd":' + str(amd[i]['total']) + ','
        s += '"intel":' + str(intel[i]['total']) + ','
        s += '"nvidia":' + str(nvidia[i]['total']) + '}'

    s = s.replace('}"', '},"')
    s = s.replace(',}', '}')
    s = s.replace('}{', '},{')
    return s

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ""

    if os.path.exists(path):
        f = open(filename)
        r = f.read()
        string = process_json(r)
        f.close()

    f = open(filename, 'w')
    f.write('[' + string + ']')
    f.close()
