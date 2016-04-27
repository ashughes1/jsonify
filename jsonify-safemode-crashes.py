import json
import os
import sys
import httplib
from datetime import date
from datetime import timedelta

MAX_DATE_RANGE = 180
SOCORRO_DOMAIN = 'crash-stats.mozilla.com'
SOCORRO_PARAMS = '/api/SuperSearch/?signature=~gfx&signature=~layers&safe_mode=1'
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


def process_json(s, max_date_range=MAX_DATE_RANGE):
    for i in range(max_date_range, -1, -1):
        end_date = str(TODAY - timedelta(days=i))

        start_dates = {
            'daily': str(TODAY - timedelta(days=i+1)),
            'weekly': str(TODAY - timedelta(days=i+7)),
            'monthly': str(TODAY - timedelta(days=i+30))
        }

        params = {
            'daily': '{0}&date=%3E%3D{1}&date=%3C{2}'.format(SOCORRO_PARAMS, start_dates['daily'], end_date),
            'weekly': '{0}&date=%3E%3D{1}&date=%3C{2}'.format(SOCORRO_PARAMS, start_dates['weekly'], end_date),
            'monthly': '{0}&date=%3E%3D{1}&date=%3C{2}'.format(SOCORRO_PARAMS, start_dates['monthly'], end_date)
        }

        totals = {
            'daily': get_json(SOCORRO_DOMAIN, params['daily'])['total'],
            'weekly': get_json(SOCORRO_DOMAIN, params['weekly'])['total'],
            'monthly': get_json(SOCORRO_DOMAIN, params['monthly'])['total']
        }

        if end_date not in s:
            #s += '{"date":"{0}","daily":{1},"weekly":{2},"monthly":{3}}'.format(end_date, str(totals['daily']), str(totals['weekly']), str(totals['monthly']))
            s += '{"date":"' + end_date + '","daily":' + str(totals['daily']) + ',"weekly":' + str(totals['weekly']) + ',"monthly":' + str(totals['monthly']) + '}'


        progress = int((float(max_date_range) - float(i)) / float(max_date_range) * 100)
        sys.stdout.write("Processing: %d%% \r" % (progress))
        sys.stdout.flush()

        result = '[{0}]'.format(s.replace('}{', '},{'))
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
        string = process_json(f.strip('[]'),1)
    else:
        string = process_json('',1)

    f = open(filename, 'w')
    f.write(string)
    f.close()
