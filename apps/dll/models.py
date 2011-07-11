from django.db import models
from django.contrib.auth.models import User
import datetime

class File(models.Model):
    """The actual DLL file itself"""
    STATUS_UNKNOWN = 'unknown'
    STATUS_VALID = 'valid'
    STATUS_MALWARE = 'malware'
    STATUS_CHOICES = (
        (STATUS_UNKNOWN, 'Unknown'),
        (STATUS_VALID,     'Valid'),
        (STATUS_MALWARE, 'Malware')
    )
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_modified = models.DateTimeField(default=datetime.datetime.now, 
                                         auto_now=True)
    created_by = models.ForeignKey(Users)
    file_name = models.CharField(max_length=200)
    common_name = models.CharField(max_length=200, blank=True, null=True)
    vendor = models.CharField(max_length=200, blank=True, null=True)
    distributors = models.CharField(max_length = 200, blank=True, null=True)
    md5_hash = models.CharField(max_length = 32, blank=True, null=True)
    sha1_hash = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    released = models.DateField(blank=True, null=True)
    obsolete = models.BooleanField(default=False)
    replaced_by = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    

class Comment(models.Model):
    """Comments users have made on given DLL files"""
    user = models.ForeignKey(User)
    dll = models.ForeignKey(File)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()    

class FileHistory(models.Model):
    """A historical record of the DLL file and the changes made to it over 
       time"""
    dllid = models.ForeignKey(File)
    user = models.ForeignKey(Users)
    date_changed = models.DateTimeField(auto_now=True)
    field = models.CharField(max_length=40)
    original_state = models.CharField(max_length=200)
    changed_state = models.CharField(max_length=200)