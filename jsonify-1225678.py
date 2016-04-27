import json
import os
import sys
import httplib
from datetime import date
from datetime import timedelta

MAX_DATE_RANGE = 180
SOCORRO_DOMAIN = 'crash-stats.mozilla.com'
SOCORRO_PARAMS = '/api/SuperSearch/?product=Firefox&signature=%3DnsGlobalWindow%3A%3ASetDocShell'
TODAY = date.today()

def get_json(server=SOCORRO_DOMAIN, params=SOCORRO_PARAMS):
    connection = httplib.HTTPSConnection(server)
    connection.request('GET', params)
    response = connection.getresponse()
    try:
        data = json.load(response)
        connection.close()
    except:
        print("WARNING: No JSON data returned for https://{0}{1} | Reattempting...").format(server, params)
        connection.close()
        data = get_json(server, params)
    return data

def process_json(string):
    today = date.today()

    for i in range(180,-1,-1):
        start_date = str(today-timedelta(days=i+1))
        end_date = str(today-timedelta(days=i))
        if start_date not in string:
            params = SOCORRO_PARAMS + '&date=>%3D' + start_date + '&date=<' + end_date
            data = get_json(SOCORRO_DOMAIN, params)
            string += '{"date":"' + end_date + '","total":' + str(data['total']) + '}'
        progress = int((float(180) - float(i)) / float(180) * 100)
        sys.stdout.write("Processing: " + SOCORRO_DOMAIN + params + " [%d%%] \r" % (progress) )
        sys.stdout.flush()

    result = '[{0}]'.format(string.replace('}{', '},{'))
    return result

# Main program
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

    f = open(filename, 'w')
    f.write(string)
    f.close()
