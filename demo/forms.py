from django import forms
from django.forms import ModelForm
import datetime
from tagging.forms import TagField

class AddTagsForm(forms.Form):
    tags = TagField()
