import httplib, json, os, requests, sys, urllib2
from datetime import date, datetime, timedelta

TODAY = date.today()
SERVER = 'bugzilla.mozilla.org'
PARAMS = '/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&resolution=---'

def get_json(server=SERVER, params=PARAMS):
    print server, params
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

def process_json(string, max_range):
    for i in range(max_range,-1,-1):
        deltas = [
            {'period':'0-3 months','start':TODAY-timedelta(days=i+1),'end':TODAY-timedelta(days=i+90)},
            {'period':'3-6 months','start':TODAY-timedelta(days=i+90),'end':TODAY-timedelta(days=i+180)},
            {'period':'6-12 months','start':TODAY-timedelta(days=i+180),'end':TODAY-timedelta(days=i+365)},
            {'period':'1-2 years','start':TODAY-timedelta(days=i+365),'end':TODAY-timedelta(days=i+730)},
            {'period':'2+ years','start':TODAY-timedelta(days=i+730),'end':''}
        ]

        string += '{"date":"' + str(deltas[0]['start']) + '",'
        for d in deltas:
            url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&status=RESOLVED&chfield=[Bug creation]&chfieldfrom=' + str(d['end']) + '&chfieldto=' + str(d['start']) + '&include_fields=id'
            json = requests.get(url).json()
            total = len(json['bugs'])
            string += '"' + d['period'] + '":' + str(total) + ','
        string += '}'

    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
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
        string = process_json(f.strip('[]'),3)
    else:
        string = process_json('',3)

    print string
    # f = open(filename, 'w')
    # f.write(string)
    # f.close()
