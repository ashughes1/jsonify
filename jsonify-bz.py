import json
import os
import sys
import urllib2
from datetime import date
from datetime import timedelta

class Query():
    def __init__(self):
        print "query!"

class BugzillaQuery():
    def __init__(self, url):
        self.url = url
        self.response = urllib2.urlopen(self.url)
        self.data = json.load(self.response)
        self.bug_count = len(self.data['bugs'])

    def get_data(self):
        return self.data

    def get_bug_count(self):
        return self.bug_count



url = 'https://bugzilla.mozilla.org/rest/bug?product=Core&component=Canvas%3A+2D&component=Canvas%3A+WebGL&component=GFX%3A+Color+Management&component=Graphics&component=Graphics%3A+Layers&component=Graphics%3A+Text&component=Image+Blocking&component=ImageLib&component=Panning+and+Zooming&f1=cf_status_firefox42&o1=nowordssubstr&v1=---%2C+unaffected&f2=cf_status_firefox42&o2=isnotempty&v2=&chfield=[Bug+creation]&chfieldvalue=&chfieldfrom=2015-10-20&chfieldto=now'  # noqa
bugzilla = BugzillaQuery(url)

print bugzilla.url
print str(bugzilla.get_bug_count())
