#Embedded file name: /Users/brandon/Sites/dlldir/project/dll/cron.py
import cronjobs
import csv
import urllib
import datetime
from dragnet.dll.models import File
from django.contrib.auth.models import User
from django.db import IntegrityError

class ImproperStatusCode(Exception):
    pass


@cronjobs.register
def updateModuleData():
    yesterday = datetime.date.today() - datetime.timedelta(2)
    reportdatestring = yesterday.strftime('%Y%m%d')
    baseurl = 'https://crash-analysis.mozilla.com/crash_analysis/modulelist/%s-modulelist.txt' % reportdatestring
    webpage = urllib.urlopen(baseurl)
    code = webpage.getcode()
    if code != 200:
        raise ImproperStatusCode('Status code for %s was: %s' % (baseurl, code))
    datareader = csv.reader(webpage)
    data = []
    for row in datareader:
        data.append(row)

    sysuser = User.objects.get(username='system')
    for x in data:
        try:
            File.objects.create(created_by=sysuser, modified_by=sysuser, file_name=x[0], debug_filename=x[1], debug=x[2], version=x[3])
        except IntegrityError:
            pass

    return 0
