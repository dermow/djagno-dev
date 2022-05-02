'''views'''
from django.http import HttpResponse
from django.shortcuts import render
from gemplanner.models import Quest, QuestRewardMapping, SkillGem

def index(request):
    '''base view'''
    return HttpResponse(f"page is under construction")

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
