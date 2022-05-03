from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quests', views.quests, name='quests'),
    path('gems', views.gems, name='gems'),
    path('mappings', views.mappings, name='mappings'),
]