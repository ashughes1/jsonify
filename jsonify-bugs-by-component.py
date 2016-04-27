import httplib, json, os, requests, sys, time, urllib2
from datetime import date, datetime, timedelta

TODAY = date.today()
SERVER = 'bugzilla.mozilla.org'
PARAMS = '/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&resolution=---'

def get_json(url):
    try:
        json = requests.get(url).json()
    except:
        print('WARNING: No data for {} | Reattempting...').format(url)
        json = get_json(url)
    return json

def process_json(string, max_range):
    print '[' + time.strftime('%H:%M:%S') + '] STARTED PROCESSING DATA!'
    for d in range(120, -1, -1):
        max_date = TODAY - timedelta(days=d)
        counts = {
            'Canvas: 2D': 0,
            'Canvas: WebGL': 0,
            'GFX: Color Management': 0,
            'Graphics': 0,
            'Graphics: Layers': 0,
            'Graphics: Text': 0,
            'Image Blocking': 0,
            'ImageLib': 0,
            'Panning and Zooming': 0,
            'Total': 0
        }

        for i in range(2000, max_date.year+1):
            start = str(i) + '-01-01'
            end = str(i) + '-12-31'
            if (i == max_date.year):
                end = str(max_date)

            # RESOLVED BUGS
            # url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&status=RESOLVED&chfield=[Bug creation]&chfieldfrom=' + start + '&chfieldto=' + end + '&f1=cf_last_resolved&o1=lessthan&v1=' + str(TODAY-timedelta(days=d)) + '&include_fields=id'
            # json = get_json(url)
            # resolved += len(json['bugs'])

            # UNRESOLVED BUGS
            url = 'https://' + SERVER + '/rest/bug?product=Core&component=Canvas%3A 2D&component=Canvas%3A WebGL&component=GFX%3A Color Management&component=Graphics&component=Graphics%3A Layers&component=Graphics%3A Text&component=Image Blocking&component=ImageLib&component=Panning and Zooming&resolution=---&chfield=[Bug creation]&chfieldfrom=' + start + '&chfieldto=' + end + '&include_fields=component'
            json = get_json(url)

            for b in json['bugs']:
                counts[b['component']] += 1

        string += '{"date":"' + str(TODAY-timedelta(days=d)) + '",'
        for k in sorted(counts.keys()):
            counts['Total'] += counts[k]
            string += '"' + k + '":' + str(counts[k]) + ','
        string += '}'

        print '[' + time.strftime('%H:%M:%S') + '] Processed data for ' + str(max_date) + ': ' + str(counts['Total']) + ' bugs counted!'

    string = string.replace(',}', '}')
    string = string.replace('}{', '},{')
    string = '[' + string + ']'
    return string

# if len(sys.argv) <= 1:
#     print "Error> Use the following command syntax:"
#     print "python jsonify.py outfile.json"
# else:
#     filename = str(sys.argv[1])
#     path = os.getcwd() + '/' + filename
    # string = ''
    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'),365)
    # else:
    #     string = process_json('',365)

print '\n\n\n' + process_json('',365) + '\n\n\n'
    # f = open(filename, 'w')
    # f.write(string)
    # f.close()
