import cronjobs
import csv
import urllib
import datetime
import logging
from dragnet.dll.models import File
from django.contrib.auth.models import User

logger = logging.getLogger("import")


class ImproperStatusCode(Exception):
    pass


@cronjobs.register
def update_module_data():
    last_report = (datetime.datetime.utcnow() -
                    datetime.timedelta(days=2)).date()
    report_date_string = last_report.strftime('%Y%m%d')
    baseurl = (
        'https://crash-analysis.mozilla.com/crash_analysis/modulelist/'
        '%s-modulelist.txt' % report_date_string
    )
    webpage = urllib.urlopen(baseurl)
    code = webpage.getcode()
    if code != 200:
        raise ImproperStatusCode('Status code for %s was: %s' %
                                    (baseurl, code))
    datareader = csv.reader(webpage)

    # System user is created when the database is created.
    sys_user, sys_user_created = User.objects.get_or_create(
        username='system',
        first_name='System',
    )

    if sys_user_created:
        sys_user.save()

    for row in datareader:
        try:
            File.objects.create(
                created_by=sys_user,
                modified_by=sys_user,
                file_name=row[0],
                debug_filename=row[1],
                debug=row[2],
                version=row[3]
            )
        except Exception, err:
            logger.info('Import error: %s', err)
    return 0
