from django.db import models

class Comments(models.Model):
    user_id = models.ForeignKey('Users')
    dll_id = models.ForeignKey('DllFile')
    date = models.DateTimeField(auto_now_add = True)
    comment = models.TextField()
    
    
class Users(models.Model):
    display_name = models.TextField()
    permissions = models.CharField(max_length = 8)
    
class DllFile(models.Model):
    STATUS_CHOICES = (
        ('0', 'Unknown'),
        ('1', 'Valid'),
        ('2', 'Malware')
    )
    date_created = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey('Users')
    file_name = models.CharField(max_length = 200)
    common_name = models.CharField(max_length = 200, blank = True)
    vendor = models.CharField(max_length = 200, blank = True)
    distributors = models.CharField(max_length = 200, blank = True)
    md5_hash = models.CharField(max_length = 32, blank = True)
    sha1_hash = models.CharField(max_length=40, blank = True)
    status = models.CharField(max_length = 1, choices = STATUS_CHOICES)
    released = models.DateField(blank = True)
    obsolete = models.BooleanField()
    replaced_by = models.CharField(max_length = 200, blank = True)
    details = models.TextField(blank = True)
    
class DllHistory(models.Model):
    dllid = models.ForeignKey('DllFile')
    userid = models.ForeignKey('Users')
    date = models.DateTimeField(auto_now = True)
    field = models.CharField(max_length = 40)
    original_state = models.CharField(max_length = 200)
    changed_state = models.CharField(max_length = 200)