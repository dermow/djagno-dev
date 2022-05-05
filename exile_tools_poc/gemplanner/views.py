'''views'''
import base64
from webbrowser import get
from django.http import HttpResponse
from django.shortcuts import render
from gemplanner.models import Quest, QuestRewardMapping, SkillGem
import requests
import zlib
import xml.etree.ElementTree as ET

from . import forms
from . import models

def index(request):
    '''base view'''
    form = forms.PasteBinForm()
    pb_url = ""
    pb_data = ""
    decompressed = ""
    decoded = ""
    gems = []
    data = { 
        'class': 'scion',
        'gems': [],
        'not_found': [],
        'instructions': [],
        }

    if request.method == 'POST':
        if request.POST['pastebin_url']:
            pb_code = request.POST['pastebin_url'].split('/')[-1]
            pb_url = f"https://pastebin.com/raw/{pb_code}"
            r_pb = requests.get(pb_url)
            pb_data = r_pb.text.replace('_', '/').replace('-', '+')
            decoded = base64.b64decode(pb_data)
            decompressed = zlib.decompress(decoded).decode('UTF-8')
            xml = ET.fromstring(decompressed)
            for node in xml:
                if node.tag == 'Build':
                    data['class'] = node.attrib['className']
                
                    
                if node.tag == 'Skills':
                    for skillGroupNode in node:
                        for gemNode in skillGroupNode:
                            gem_name = gemNode.attrib['nameSpec']
                            gem_id = gemNode.attrib['skillId']
                            try:
                                if 'Support' in gem_id:
                                    gem_name = f"{gem_name} Support"
                                gem_object = SkillGem.objects.get(name=gem_name)
                                data['gems'].append(gem_object.id)
                            except SkillGem.DoesNotExist:
                                data['not_found'].append(gem_name)

            for item in data['gems']:
                gem = SkillGem.objects.get(id=item)
                mappings = QuestRewardMapping.objects.filter(class_name=data['class'], gem=gem, achieve_type='reward')
                if len(mappings):
                    mapping = mappings[0]
                    data['instructions'].append(f'get {gem.name} in {mapping.quest.act}, after completing quest: {mapping.quest.title}')
                

    return render(request, 'planner/planner.html', {'form': form, 'request': request, 'data': data})

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
