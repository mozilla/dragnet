"""Example views. Feel free to delete this app."""

from django import http
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import bleach
import jingo

from dll.forms import *
from dll.models import *

def home(request):
    dlls = File.objects.all().order_by('-date_modified')[:10]
    count = File.objects.count()
    search = SearchForm()
    data = {'dlls' : dlls, 'count' : count, 'search': search}
    return jingo.render(request, 'dll/index.html', data)
    
def search(request):
    search = SearchForm(request.POST)
    if search.is_valid():
        term = search.cleaned_data['search']
    else:
        http.HttpResponseRedirect('/')
    results = File.objects.filter(file_name__contains=term)
    data = {'count': len(results), 'dlls': results, 'term' : term, 'search': search}
    return jingo.render(request, 'dll/search.html', data)
    
def create(request):
    """Main view."""
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FileForm()
    data = {'form':form}
    return jingo.render(request, 'dll/createedit.html', data)

def edit(request, dllname):
    thefile = get_object_or_404(File, file_name__exact=dllname)
    if request.method == 'POST':
        form = FileForm(request.POST, instance=thefile)
        if form.is_valid():
            form.save()
    else:
        form = FileForm(instance = thefile)
    data = {'dllname': dllname, 'form':form}
    return jingo.render(request, 'dll/createedit.html', data)