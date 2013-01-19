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
    last_report = datetime.date.today() - datetime.timedelta(days=2)
    reportdatestring = last_report.strftime('%Y%m%d')
    baseurl = ('https://crash-analysis.mozilla.com/crash_analysis/modulelist/'
                '%s-modulelist.txt' % reportdatestring)
    webpage = urllib.urlopen(baseurl)
    code = webpage.getcode()
    if code != 200:
        raise ImproperStatusCode('Status code for %s was: %s' % (baseurl, code))
    datareader = csv.reader(webpage)

    # System user is created when the database is created.
    sysuser = User.objects.get(username='system')
    for row in datareader:
        try:
            File.objects.create(created_by=sysuser, modified_by=sysuser, file_name=row[0], debug_filename=row[1], debug=row[2], version=row[3])
        except IntegrityError:
            # When a module is already in the database it cannot be added
            # again. It will raise an IntegrityError on the unique index,
            # which is expected behavior. This is a safe exception to ignore.
            pass

    return 0
