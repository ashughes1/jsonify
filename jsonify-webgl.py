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

    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            url = 'https://crash-stats.mozilla.com/api/SuperSearch/?date=%3E%3D' + start_date + '&date=%3C' + end_date + '&app_notes=webgl&_columns=platform_pretty_version&_columns=app_notes'
            facets = get_json(url)
            webgl = {'+':0, '-':0, '?':0}


            for hit in facets['hits']:
                try:
                    notes = str(hit['app_notes'])
                except:
                    notes = ''

                if notes.count('WebGL+'):
                    webgl['+'] += 1
                if notes.count('WebGL-'):
                    webgl['-'] += 1
                if notes.count('WebGL?'):
                    webgl['?'] += 1

            string += '{"date":"' + start_date + '",'
            string += '"webgl?":' + str(webgl['?']) + ','
            string += '"webgl+":' + str(webgl['+']) + ','
            string += '"webgl-":' + str(webgl['-']) + '}'

        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Progress: %d%% \r" % (progress) )
        sys.stdout.flush()

    string = string.replace('}"', '},"')
    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
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
