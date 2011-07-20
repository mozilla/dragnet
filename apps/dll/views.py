"""Example views. Feel free to delete this app."""

from django import http
from django.views.decorators.csrf import csrf_exempt

import bleach
import jingo

from dll.forms import *
from dll.models import *


def home(request):
    """Main view."""
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FileForm()
    data = {'form':form}
    return jingo.render(request, 'dll/home.html', data)

def edit(request, dllid):
    thefile = File.objects.get(pk=dllid)
    if request.method == 'POST':
        form = FileForm(request.POST, instance=thefile)
        if form.is_valid():
            form.save()
    else:
        form = FileForm(instance = thefile)
    data = {'dllid': dllid, 'form':form}
    return jingo.render(request, 'dll/home.html', data)