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
    today = date.today()-timedelta(days=1)
    
    data = {
        'webgl_all':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~WebGL&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'webgl_success':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~WebGL%2B&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'webgl_fail':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~WebGL-&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'webgl_attempt':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?app_notes=~WebGL%3F&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'all_crashes':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d')
    }
    
        
    for d in data['all_crashes']['facets']['histogram_date']:
        datestamp = d['term'][0:10]
        counts = {
            'webgl_all':0,
            'webgl_success':0,
            'webgl_fail':0,
            'webgl_attempt':0,
            'all_crashes':0
        }   
        
        for key in data.keys():
            for c in data[key]['facets']['histogram_date']:
                if c['term'] == d['term']:
                    counts[key] = c['count']
        
        attempt = '{:.2f}'.format(float(counts['webgl_attempt'])/float(counts['all_crashes'])*100)
        success = '{:.2f}'.format(float(counts['webgl_success'])/float(counts['all_crashes'])*100)
        fail = '{:.2f}'.format(float(counts['webgl_fail'])/float(counts['all_crashes'])*100)
        
        string += '{'
        string += '"date":"{:s}","webgl?":{:s},"webgl+":{:s},"webgl-":{:s}'.format(datestamp,attempt,success,fail)
        string += '}'
    
    # for d in data['json']['facets']['histogram_date']:
    #     counts = {
    #         'amd':0,
    #         'intel':0,
    #         'nvidia':0,
    #         'android':0
    #     }
    #     for vendor in firefox_data['facets']['adapter_vendor_id']:
    #         if vendor['term'] == '0x8086':
    #             counts['intel'] = vendor['count']
    #         elif vendor['term'] == '0x1002':
    #             counts['amd'] = vendor['count']
    #         elif vendor['term'] == '0x10de':
    #             counts['nvidia'] = vendor['count']
    #     for android_data in fennec['data']['facets']['histogram_date']:
    #         if android_data['term'] == firefox_data['term']:
    #             counts['android'] = android_data['count']
    #     string += '{"date":"' + firefox_data['term'][0:10] + '"' + ',"amd":' + str(counts['amd']) + ',"intel":' + str(counts['intel']) + ',"nvidia":' + str(counts['nvidia']) + ',"android":' + str(counts['android']) + '}'
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
