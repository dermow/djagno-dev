from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .forms import MyForm

# Create your views here.
def index(request):
    form = MyForm()
    entries = ["test", "test2", "test3"]
    return render(request, 'testui/index.html', {'form': form, 'entries': entries})
