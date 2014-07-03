from django import forms
from django.contrib import admin
from django.forms import ModelForm

from django_markdown.widgets import MarkdownWidget
from flatblocks.admin import FlatBlockAdmin
from flatblocks.models import FlatBlock


class LocalFlatBlockForm(ModelForm):
    content = forms.CharField(widget=MarkdownWidget)

    class Meta:
        model = FlatBlock


class LocalFlatBlcokAdmin(FlatBlockAdmin):
    form = LocalFlatBlockForm


def register():
    admin.site.unregister(FlatBlock)
    admin.site.register(FlatBlock, LocalFlatBlcokAdmin)
