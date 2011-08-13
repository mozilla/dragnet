import jingo
import jinja2
import forms
from babel.dates import format_date, format_datetime

@jingo.register.function
def BasicSearchForm(request):
    if 'term' in request.GET:
        data = {'term': request.GET['term']}
    else:
        data = {'term': 'Search'}
    form = forms.SearchForm(data)
    return form
    
@jingo.register.function
def dll_date_format(date):
    return format_date(date)

@jingo.register.function
def dll_datetime_format(date):
    return format_datetime(date)