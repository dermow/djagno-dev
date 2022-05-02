from django.db import models

# Create your models here.
class SkillGem(models.Model):
    '''Skill Gem'''
    name = models.CharField(max_length=100)

class Quest(models.Model):
    '''Quest'''
    title = models.CharField(max_length=100)
    act = models.CharField(max_length=10, default="")
    description = models.CharField(max_length=100, default="")
    url = models.URLField(default="")

class QuestRewardMapping(models.Model):
    '''Reward Mapping'''
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    gem = models.ForeignKey(SkillGem, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, default='Scion')
    achieve_type = models.CharField(max_length=10, default='reward')
