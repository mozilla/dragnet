from django.forms import ModelForm
from dll import models as dllmodel

class FileForm(ModelForm):
    class Meta:
        model = dllmodel.File
        
        