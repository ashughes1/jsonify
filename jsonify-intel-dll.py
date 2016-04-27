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
    today = date.today()

    for i in range(0,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            url = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&signature=~igd10iumd32.dll&signature=~igd10umd32.dll&signature=~igdumd32.dll&signature=~igdumd64.dll&signature=~igd10iumd64.dll&_facets=release_channel'
            data = get_json(url)
            print data
        #     string += '{"date":"' + start_date + '",'
        #     string += '"nightly":' + str(totals['nightly']) + ','
        #     string += '"aurora":' + str(totals['aurora']) + ','
        #     string += '"beta":' + str(totals['beta']) + ','
        #     string += '"release":' + str(totals['release']) + '}'
        # progress = int((float(180) - float(i)) / float(180) * 100)
        # sys.stdout.write("Progress: %d%% \r" % (progress) )
        # sys.stdout.flush()
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    string = ''
    if os.path.exists(path):
        f = open(filename).read()
        string = process_json(f.strip('[]'))
    else:
        string = process_json('')

    # string = string.replace('}{', '},{')
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
