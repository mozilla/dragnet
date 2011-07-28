from django import forms
from dll.models import File, Comment


class FileForm(forms.ModelForm):
    """Using a model form to expedite the creation of DLL records"""
    class Meta:
        model = File
        exclude = ('date_created', 'date_modified',
        #'created_by',
        #           'modified_by', )
        )


class CommentForm(forms.ModelForm):
    """Comment form for DLL comments"""
    class Meta:
        model = Comment
        exclude = ('user', 'dll', 'date', )


class SearchForm(forms.Form):
    term = forms.CharField()
