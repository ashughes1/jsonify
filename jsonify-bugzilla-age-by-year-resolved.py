import httplib, json, os, requests, sys, time, urllib2
from datetime import date, datetime, timedelta

TODAY = date.today()
SERVER = 'bugzilla.mozilla.org'
PARAMS = '/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&resolution=---'

# def get_json(server=SERVER, params=PARAMS):
#     print server, params
#     connection = httplib.HTTPSConnection(server)
#     connection.request('GET', params)
#     response = connection.getresponse()
#     try:
#         data = json.load(response)
#         connection.close()
#     except:
#         print("WARNING: No JSON data returned for https://{0}{1} | Reattempting...").format(server, params)
#         connection.close()
#         data = get_json(server, params)
#     return data

def get_json(url):
    try:
        json = requests.get(url).json()
    except:
        print('WARNING: No data for {} | Reattempting...').format(url)
        json = get_json(url)
    return json

def process_json(string, max_range):
    print '[' + time.strftime('%H:%M:%S') + '] STARTED PROCESSING DATA!'
    for d in range(1195, 1095, -1):
        max_date = TODAY - timedelta(days=d)
        resolved = 0
        unresolved = 0

        for i in range(2000, max_date.year+1):
            start = str(i) + '-01-01'
            end = str(i) + '-12-31'
            if (i == max_date.year):
                end = str(max_date)

            # RESOLVED BUGS
            url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&status=RESOLVED&chfield=[Bug creation]&chfieldfrom=' + start + '&chfieldto=' + end + '&f1=cf_last_resolved&o1=lessthan&v1=' + str(TODAY-timedelta(days=d)) + '&include_fields=id'
            json = get_json(url)
            resolved += len(json['bugs'])

            # UNRESOLVED BUGS
            url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=' + start + '&chfieldto=' + end + '&include_fields=id'
            json = get_json(url)
            unresolved += len(json['bugs'])

        percent_resolved = round(float(resolved)/float(resolved+unresolved)*100, 2)
        string += '{"date":"' + str(TODAY-timedelta(days=d)) + '","resolved":' + str(resolved) + ',"unresolved":' + str(unresolved) + ',"percent":' + str(percent_resolved) + '}'
        print '[' + time.strftime('%H:%M:%S') + '] Processed data for ' + str(max_date) + ': ' + str(resolved) + ', ' + str(unresolved) + ', ' + str(percent_resolved) + '% ..... '

    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
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
        string = process_json(f.strip('[]'),365)
    else:
        string = process_json('',365)

    print '\n\n\n' + string + '\n\n\n'
    f = open(filename, 'w')
    f.write(string)
    f.close()
