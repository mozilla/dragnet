from django import http
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
import bleach
import jingo

from dll.forms import FileForm, CommentForm, SearchForm
from dll.models import File, Comment, FileHistory


def home(request):
    dlls = File.objects.all().order_by('-date_modified')[:10]
    search = SearchForm()
    data = {'dlls': dlls, 'search': search}
    return jingo.render(request, 'dll/index.html', data)

@csrf_exempt
def search(request):
    search = SearchForm(data=request.GET)
    if search.is_valid():
        term = search.cleaned_data['term']
        results = File.objects.filter(file_name__contains=term)
    else:
        term = ''
        results = []
    data = {'count': len(results), 'dlls': results, 'term': term,
            'search': search}
    return jingo.render(request, 'dll/search.html', data)


def create(request):
    """Main view."""
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FileForm()
    data = {'form': form}
    return jingo.render(request, 'dll/createedit.html', data)


def edit(request, dllname):
    thefile = get_object_or_404(File, file_name__exact=dllname)
    if request.method == 'POST':
        form = FileForm(request.POST, instance=thefile)
        if form.is_valid():
            form.save()
    else:
        form = FileForm(instance=thefile)
    data = {'dllname': dllname, 'form': form}
    return jingo.render(request, 'dll/createedit.html', data)
