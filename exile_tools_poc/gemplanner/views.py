'''views'''
import base64
from django.http import HttpResponse
from django.shortcuts import render
from gemplanner.models import Quest, QuestRewardMapping, SkillGem
import requests
import zlib

from . import forms

def index(request):
    '''base view'''
    form = forms.PasteBinForm()
    pb_url = ""
    pb_data = ""

    if request.method == 'POST':
        if request.POST['pastebin_url']:
            pb_url = request.POST['pastebin_url']
            r_pb = requests.get(pb_url)
            pb_data = r_pb.text.replace('_', '/').replace('-', '+')
            decoded = base64.b64decode(pb_data)
            decompressed = zlib.decompress(decoded).decode('UTF-8')

    return render(request, 'planner/planner.html', {'form': form, 'request': request, 'data': decompressed})

def quests(request):
    '''list of all quests'''
    entries = Quest.objects.all()
    return render(request, 'quests/quests.html', {'entries': entries})

def gems(request):
    '''list of all gems'''
    entries = SkillGem.objects.all()
    return render(request, 'gems/gems.html', {'entries': entries})

def mappings(request):
    '''list of all mappings'''
    entries = QuestRewardMapping.objects.all()
    return render(request, 'mappings/mappings.html', {'entries': entries})
