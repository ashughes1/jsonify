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
    today = date.today()-timedelta(days=363)
    data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?product=FennecAndroid&signature=~gfx&signature=~layers&signature=~canvas&signature=~GL&date=%3E%3D{:s}&_histogram.date=android_hardware&_histogram_interval=1d'.format(str(today)))
    for d in data['facets']['histogram_date']:
        datestamp = d['term']
        total = d['count']
        string += '{"date":"' + datestamp[0:10] + '","total":' + str(total)
        for hardware in d['facets']['android_hardware']:
            if hardware['term'] == 'qcom':
                string += ',"qcom":{:d}'.format(hardware['count'])
            elif hardware['term'] == 'smdk4x12':
                string += ',"smdx4x12":{:d}'.format(hardware['count'])
            elif hardware['term'] == 'universal5420':
                string += ',"universal5420":{:d}'.format(hardware['count'])
            elif hardware['term'] == 'espresso10':
                string += ',"espresso10":{:d}'.format(hardware['count'])
        string += '}' 

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
