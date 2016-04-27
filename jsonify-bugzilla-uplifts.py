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
    today = date.today()
    domain = 'https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'
    totals = {'release':0,'beta':0,'aurora':0}
    merges = ['2016-03-08','2016-01-26','2015-12-15','2015-11-03','2015-09-22','2015-08-11','2015-06-30','2015-05-12','2015-03-31']
    for i in range(365,1,-1):
        start_date = str(today-timedelta(days=i))
        end_date = str(today-timedelta(days=i))
        data = {
            'release':{},
            'beta':{},
            'aurora':{}
        }

        if start_date not in string:
            if start_date in merges:
                totals = {'release':0,'beta':0,'aurora':0}
            string += '{"date":"' + start_date + '",'
            for k in data.keys():
                data[k] = get_json('{0}&f1=flagtypes.name&o1=anywordssubstr&v1=approval-mozilla-{1}%2B&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom={2}&chfieldto={3}&include_fields=id'.format(domain, k, start_date, end_date))
                totals[k] = totals[k] + len(data[k]['bugs'])
            string += '"release":' + str(totals['release']) + ','
            string += '"beta":' + str(totals['beta']) + ','
            string += '"aurora":' + str(totals['aurora']) + '}'
            

        #     total_release = get_total_from_json(query_release)
        #     total_beta = get_total_from_json(query_beta)
        #     total_aurora = get_total_from_json(query_aurora)
        #
        #     string += '{"date":"' + start_date + '","release":' + total_release + ',"beta":' + total_beta + ',"aurora":' + total_aurora + '}'
        # progress = int((float(365) - float(i)) / float(365) * 100)
        # sys.stdout.write("Processing " + start_date + ": %d%% \r" % (progress) )
        # sys.stdout.flush()
    string = string.replace('}{', '},{')
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ''
    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #     string = process_json('')
    print process_json('')
