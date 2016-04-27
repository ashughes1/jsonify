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
    data = {
        'all':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=!__null__&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today))),
        'd3d9':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=~[D3D11]&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today))),
        'd3d11':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=~[D3D9]&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today))),
        'dxva':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=~DXVA&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today))),
        'glcontext':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=~GLContext&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today))),
        'texture':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?graphics_critical_error=~Texture&date=%3E%3D{:s}&_histogram.date=product&_histogram_interval=1d'.format(str(today)))
    }
    
    for d in data['all']['facets']['histogram_date']:
        datestamp = d['term']
        string += '{"date":"' + datestamp[0:10] + '"'
        for key in data.keys():
            for obj in data[key]['facets']['histogram_date']:
                if obj['term'] == datestamp:
                    string += ',"{:s}":{:d}'.format(key,obj['count'])
        string += '}' 
        


        #string += '{"date":"' + d['term'][0:10] + '"' + ',"amd":' + str(counts['amd']) + ',"intel":' + str(counts['intel']) + ',"nvidia":' + str(counts['nvidia']) + ',"total":' + str(counts['amd']+counts['intel']+counts['nvidia']) + '}'
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
