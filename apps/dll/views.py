from django import http
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
import bleach
import jingo

from dll.forms import FileForm, CommentForm, SearchForm
from dll.models import File, Comment, FileHistory
from django.core.paginator import Paginator, EmptyPage, InvalidPage

PAGE_LENGTH = 50

def home(request, page_no):
    dll_list = File.objects.all().order_by('-date_created')
    paginator = Paginator(dll_list, PAGE_LENGTH)
    try:
        page = int(page_no)
    except (ValueError, TypeError):
        page = 1

    try:
        dlls = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dlls = paginator.page(paginator.num_pages)
        
    data = {'dlls': dlls, 'last_page': paginator.num_pages,}
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
    data = {'count': len(results), 'dlls': results, 'term': term,}
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
