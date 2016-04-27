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
        'gfx':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?safe_mode=__true__&signature=~gfx&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'layers':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?safe_mode=__true__&signature=~layers&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'canvas':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?safe_mode=__true__&signature=~canvas&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d'),
        'gl':get_json('https://crash-stats.mozilla.com/api/SuperSearch/?safe_mode=__true__&signature=~gl&date=%3E%3D' + str(today) + '&_histogram.date=product&_histogram_interval.date=1d')
    }
    for d in data['facets']['histogram_date']:
        datestamp = d['term'][0:10]
        counts = {
            'firefox':0,
            'fennec':0
        }
        for product in d['facets']['product']:
            if product['term'] == 'Firefox':
                counts['firefox'] = str(product['count'])
            if product['term'] == 'FennecAndroid':
                counts['fennec'] = str(product['count'])
        
        string += '{'
        string += '"date":"{:s}","firefox":{:s},"fennec":{:s}'.format(datestamp,counts['firefox'],counts['fennec'])
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
