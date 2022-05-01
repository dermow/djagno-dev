from django.http import HttpResponse
from django.shortcuts import render
from gemplanner.models import Quest, SkillGem

def index(request):
    return HttpResponse(f"{out}")

def quests(request):
    entries = Quest.objects.all()
    return render(request, 'quests/quests.html', {'entries': entries})

def gems(request):
    entries = SkillGem.objects.all()
    return render(request, 'gems/gems.html', {'entries': entries})