from django.db import models

# Create your models here.
class SkillGem(models.Model):
    '''Skill Gem'''
    name = models.CharField(max_length=100)

class Quest(models.Model):
    '''Quest'''
    title = models.CharField(max_length=100)
    act = models.CharField(max_length=10, default="")
