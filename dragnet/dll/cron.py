import cronjobs
import csv
import urllib
import datetime
import logging
from dragnet.dll.models import File
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


logging.basicConfig()
logger = logging.getLogger("cron")


class ImproperStatusCode(Exception):
    pass


#test

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
    
    logger.info('Now starting import...')
    
    for row in datareader:
        # We want to make the cronjob robust and not fail if we run into a
        # database error here, so we'll have a generic try-catch block that
        # captures all unexpected errors and logs them.
        #
        # Otherwise, an exception would cause the job to fail, and it would
        # have to be rerun manually.
        #
        # We will catch and handle all known exception types explicitly.
        try:
            try:
                file_ = File.objects.get(file_name=row[0],
                                         debug_filename=row[1],
                                         debug=row[2]
                                         )
            except ObjectDoesNotExist:            
                File.objects.create(
                    created_by=sys_user,
                    modified_by=sys_user,
                    file_name=row[0],
                    debug_filename=row[1],
                    debug=row[2],
                    version=row[3]
                )
        except Exception:
            logger.error('Import failed on %s' % row[0], exc_info=True)
    
    logger.info('Import is complete')
    return 0
