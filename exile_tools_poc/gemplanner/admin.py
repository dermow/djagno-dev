from django.contrib import admin

from .models import QuestRewardMapping, SkillGem, Quest

admin.site.register(SkillGem)
admin.site.register(Quest)
admin.site.register(QuestRewardMapping)