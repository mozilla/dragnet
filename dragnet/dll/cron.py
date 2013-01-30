import cronjobs
import csv
import urllib
import datetime
import logging
from dragnet.dll.models import File
from django.contrib.auth.models import User
from django.db import IntegrityError

logger = logging.getLogger("cron")


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
        logger.error('Response from %s was %s', baseurl, webpage)
        raise ImproperStatusCode('Status code for %s was: %s' %
                                    (baseurl, code))
    datareader = csv.reader(webpage)

    sys_user, ___ = User.objects.get_or_create(
        username='system',
        first_name='System',
    )

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
        except IntegrityError:
            logger.info('Integrity error', exc_info=True)
    return 0
