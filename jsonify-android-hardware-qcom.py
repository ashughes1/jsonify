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
    data = get_json('https://crash-stats.mozilla.com/api/SuperSearch/?product=FennecAndroid&android_hardware=qcom&signature=~gfx&signature=~layers&signature=~canvas&signature=~GL&date=%3E%3D{:s}&_histogram.date=android_model&_histogram_interval=1d'.format(str(today)))
    
    # get a list of all devices
    devices = {}
    print "DEVICES LIST GENERATING!"
    for d in data['facets']['histogram_date']:
        for model in d['facets']['android_model']:
            found = 0
            if devices.has_key(model['term']):
                devices[model['term']] += model['count']
            else:
                devices[model['term']] = model['count']
    
    top_devices = {}
    for key in devices.keys():
         if devices[key] > 11500:
             top_devices[key] = 0
    print top_devices
    
    # print "JSON GENERATION STARTED!"
    # for d in data['facets']['histogram_date']:
    #     datestamp = d['term']
    #     string += '{"date":"' + datestamp[0:10] + '"'
    #     print "PROCESSING DATA FOR " + datestamp
    #     for model in d['facets']['android_model']:
    #         if top_devices.has_key(model['term']):
    #             string += ',"{:s}":{:d}'.format(model['term'],model['count'])
    #     string += '}'
    # print "JSON GENERATION COMPLETED!"
                    
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
