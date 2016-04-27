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

def process_json(string):
    #domain = 'https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'
    #if start_date not in string:
    string = '[{"date":"' + str(TODAY) + '",'

    # 0-3 months
    url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=-3m&chfieldto=Now&include_fields=id'
    json = requests.get(url).json()
    total = len(json['bugs'])
    string += '"0-3 months":' + str(len(json['bugs'])) + ','

    # 3-6 months
    url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=-6m&chfieldto=-3m&include_fields=id'
    json = requests.get(url).json()
    total = len(json['bugs'])
    string += '"3-6 months":' + str(len(json['bugs'])) + ','

    # 6-12 months
    url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=-1y&chfieldto=-6m&include_fields=id'
    json = requests.get(url).json()
    total = len(json['bugs'])
    string += '"6-12 months":' + str(len(json['bugs'])) + ','

    # 1-2 years
    url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=-2y&chfieldto=-1y&include_fields=id'
    json = requests.get(url).json()
    total = len(json['bugs'])
    string += '"12-24 months":' + str(len(json['bugs'])) + ','

    # 2+ years
    url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldto=-2y&include_fields=id'
    json = requests.get(url).json()
    total = len(json['bugs'])
    string += '"2+ years":' + str(len(json['bugs']))

    string += '}]'

    return string.replace('}{', '},{')

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
