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
    start_date = str(date.today()-timedelta(days=200))

    url = {
        'amd': 'https://crash-stats.mozilla.com/api/SuperSearch/?signature=~amdocl.dll&signature=~amdocl64.dll&signature=~aticfx32.dll&signature=~atidxx32.dll&signature=~atioglxx.dll&signature=~atiu9pag.dll&signature=~atiumd64.dll&signature=~atiumd6a.dll&signature=~atiumdag.dll&signature=~atiumdva.dll&signature=~atiuxpag.dll&signature=~atidxx64.dll&signature=~atiumd64.dll&date=%3E%3D' + start_date + '&_histogram.date=release_channel&histogram_interval=1d',
        'intel': 'https://crash-stats.mozilla.com/api/SuperSearch/?signature=~igd10iumd32.dll&signature=~igd10umd32.dll&signature=~igdumd32.dll&signature=~igdumd64.dll&signature=~igd10iumd64.dll&date=%3E%3D' + start_date + '&_histogram.date=release_channel&histogram_interval=1d',
        'nvidia':'https://crash-stats.mozilla.com/api/SuperSearch/?signature=~nvwgf2um.dll&signature=~nvumdshim.dll&signature=~nvapi.dll&signature=~nvd3dum.dll&signature=~nvlsp.dll&signature=~nvlsp64.dll&date=%3E%3D' + start_date + '&_histogram.date=release_channel&histogram_interval=1d'
    }
    
    data = {
        'amd':get_json(url['amd']),
        'intel':get_json(url['intel']),
        'nvidia':get_json(url['nvidia'])
    }

    result = {
        'amd':[],
        'intel':[],
        'nvidia':[]
    }

    for k in sorted(url.keys()):
        for d in data[k]['facets']['histogram_date']:
            item = {'date':str(d['term'][0:10]), 'release':0, 'beta':0, 'aurora':0, 'nightly':0}
            for channel in d['facets']['release_channel']:
                if channel['term'] == 'nightly' or channel['term'] == 'aurora' or channel['term'] == 'beta' or channel['term'] == 'release':
                    item[channel['term']] = channel['count']
            result[k].append(item)
    
    string = str(result)
    string = string.replace(' ', '')
    string = string.replace('\'', '"')
    return string

if len(sys.argv) <= 1:
    print "Error> Use the following command syntax:"
    print "python jsonify.py outfile.json"
else:
    filename = str(sys.argv[1])
    path = os.getcwd() + '/' + filename
    print process_json('')
    # if os.path.exists(path):
    #     f = open(filename).read()
    #     string = process_json(f.strip('[]'))
    # else:
    #    string = process_json('')

    # string = string.replace('}{', '},{')
    # f = open(filename, 'w')
    # f.write('[' + string + ']')
    # f.close()
