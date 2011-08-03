import jingo
import jinja2
import forms
from babel.dates import format_date, format_datetime

@jingo.register.function
def BasicSearchForm(request):
    data = request.GET
    form = forms.SearchForm(data)
    return data
    
@jingo.register.function
def dll_date_format(date):
    return format_date(date)

@jingo.register.function
def dll_datetime_format(date):
    return format_datetime(date)