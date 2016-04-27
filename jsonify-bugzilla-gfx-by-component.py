import json
import os
import sys
import urllib2
import requests
from datetime import date
from datetime import timedelta

def get_total_from_json(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    return str(len(data['bugs']))

def process_json(string):
    today = date.today()
    domain = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,component&product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming'

    data = {
        'all':0,
        'Canvas: 2D':0,
        'Canvas: WebGL':0,
        'GFX: Color Management':0,
        'Graphics':0,
        'Graphics: Layers':0,
        'Graphics: Text':0,
        'Image Blocking':0,
        'ImageLib':0,
        'Panning and Zooming':0
    }
    percents = {
        'Canvas: 2D':0,
        'Canvas: WebGL':0,
        'GFX: Color Management':0,
        'Graphics':0,
        'Graphics: Layers':0,
        'Graphics: Text':0,
        'Image Blocking':0,
        'ImageLib':0,
        'Panning and Zooming':0
    }

    for i in range(90,-1,-1):
        start_date = str(today-timedelta(days=i))
        end_date = str(today-timedelta(days=i))

        if start_date not in string:
            
            json = requests.get(domain + '&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + start_date + '&chfieldto=' + end_date).json()
            data['all'] = data['all'] + len(json['bugs'])
            
            for i in range(0, len(json['bugs'])):
                component = json['bugs'][i]['component']
                data[component] = data[component] + 1
                if not data['all'] == 0:
                    percents[component] = float(data[component])/float(data['all'])*100
                
            string += '{"date":"' + start_date + '",'
            for k in percents.keys():
                string += '"{:s}":{:.2f},'.format(k, percents[k])
            string += '}'
            
            #query_reported = domain + '&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=' + start_date + '&chfieldto=' + end_date
            #query_resolved = domain + '&chfield=bug_status&chfieldvalue=RESOLVED&chfieldfrom=' + start_date + '&chfieldto=' + end_date
            #query_duped = domain + '&chfield=resolution&chfieldvalue=DUPLICATE&chfieldfrom=' + start_date + '&chfieldto=' + end_date
            #query_reopened = domain + '&chfield=bug_status&chfieldvalue=REOPENED&chfieldfrom=' + start_date + '&chfieldto=' + end_date
#
 #           total_reported = get_total_from_json(query_reported)
  #          total_resolved = get_total_from_json(query_resolved)
   #         total_duped = get_total_from_json(query_duped)
    #        total_reopened = get_total_from_json(query_reopened)

            #string += '{"date":"' + start_date + '","reported":' + total_reported + ',"resolved":' + total_resolved + ',"duped":' + total_duped + ',"reopened":' + total_reopened + '}'
        progress = int((float(90) - float(i)) / float(90) * 100)
        sys.stdout.write("Processing " + start_date + ": %d%% \r" % (progress) )
        sys.stdout.flush()

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

    string = string.replace('}{', '},{')
    string = string.replace(',}', '}')
    print string
    
    #f = open(filename, 'w')
    #f.write('[' + string + ']')
    #f.close()
