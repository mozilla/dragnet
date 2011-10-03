import collections
from time import mktime

from django import http
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
import bleach
import jingo

from dll.forms import FileForm, CommentForm, SearchForm
from dll.models import File, Comment, FileHistory
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.db.models import Q

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
        results = File.objects.filter(Q(file_name__icontains=term) |
                                   Q(common_name__icontains=term) |
                                   Q(vendor__icontains=term) |
                                   Q(distributors__icontains=term))
    else:
        term = ''
        results = []
    data = {'count': len(results), 'dlls': results, 'term': term,}
    return jingo.render(request, 'dll/search.html', data)


def view(request, dllname):
    thefile = get_object_or_404(File, file_name__exact=dllname)
    comments = Comment.objects.order_by('date').filter(dll__exact=thefile)
    hist = FileHistory.objects.filter(dll__exact=thefile)
    history = _organize_history(hist)
    data = {'dllname': dllname, 'dlldata': thefile, 'comments': comments, 'history': history}
    return jingo.render(request, 'dll/view.html', data)
    

@login_required
def create(request):
    """Main view."""
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.modified_by = request.user
            form.save()
            return redirect('dll.edit', form.cleaned_data['file_name'])
    else:
        form = FileForm()
    data = {'form': form}
    return jingo.render(request, 'dll/create.html', data)


def edit(request, dllname):
    if not request.user.is_authenticated():
        return redirect('dll.view', dllname)
    thefile = get_object_or_404(File, file_name__exact=dllname)
    comments = Comment.objects.order_by('date').filter(dll__exact=thefile)
    hist = FileHistory.objects.filter(dll__exact=thefile)
    history = _organize_history(hist)
    form = FileForm(instance=thefile)
    comment_form = CommentForm()
    if request.method == 'POST':
        if 'update_file' in request.POST:
            form = FileForm(request.POST, instance=thefile)
            if form.is_valid():
                form.instance.modified_by = request.user
                form.save()
                return redirect('dll.edit', thefile.file_name)
        elif 'update_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                Comment.objects.create(user=request.user,
                                       dll=thefile,
                                       comment=comment_form.cleaned_data['comment'])
                return redirect('dll.edit', thefile.file_name)
    data = {'dllname': dllname, 'form': form, 'comment_form': comment_form, 'comments': comments, 'history': history}
    return jingo.render(request, 'dll/edit.html', data)


def _organize_history(resultset):
    res = collections.defaultdict(list)
    for x in resultset:
        res[x.date_changed].append(x)
    return res
        