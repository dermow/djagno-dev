'''views'''
from django.http import HttpResponse
from django.shortcuts import render
from gemplanner.models import Quest, QuestRewardMapping, SkillGem

from . import forms

def index(request):
    '''base view'''
    form = forms.SimpleGemList()
    gems = []
    mappings = []
    if request.method == 'POST':
        gems = request.POST['gem_list']
        gem_object = SkillGem.objects.get(name=gems)
        mappings = QuestRewardMapping.objects.filter(gem=gem_object)
    return render(request, 'form/form.html', {'form': form, 'request': request, 'gems': gems, 'mappings': mappings})

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
