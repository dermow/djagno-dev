'''Wiki import job'''
from email.policy import default
from django_extensions.management.jobs import DailyJob
from html.parser import HTMLParser
import requests
from gemplanner import models


class POESkillGemWikiImporter(HTMLParser):
    '''Imports skillgem information from poewiki.net'''
    skill_definition_started = True
    link_count = 0
    curr_gem_name = ""
    curr_gem_finished = False
    names = []
    data = {
        'gems': []
    }

    def handle_starttag(self, tag, attrs):
        '''Handle every new tag'''
        if tag == 'span':
            for key, value in attrs:
                if key == 'class' and value == 'c-item-hoverbox':
                    self.link_count = 0
                    self.curr_gem_name = ""

        if tag == 'a':
            if not self.skill_definition_started:
                return

            self.link_count += 1
            if self.link_count == 1:
                for key, value in attrs:
                    if key == 'title':
                        if not value in self.names:
                            self.data['gems'].append({'name': value})
                            self.names.append(value)

class POEQuestRewardWikiImporter(HTMLParser):
    '''Import gem rewards for given quest'''
    classes = [
        'Witch',
        'Shadow',
        'Ranger',
        'Duelist',
        'Marauder',
        'Templar',
        'Scion'
    ]
    class_index = 0
    first_gem_reached = False
    current_table = 'reward'
    quest = None

    def handle_data(self, data):
        if 'Vendor rewards' in data:
            self.current_table = 'vendor'

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'title':
                    try:
                        gem = models.SkillGem.objects.get(name=value)
                        self.first_gem_reached = True
                        mapping = models.QuestRewardMapping()
                        mapping.quest = self.quest
                        mapping.gem = gem
                        mapping.class_name = self.classes[self.class_index]
                        mapping.achieve_type = self.current_table
                        mapping.save()
                    except models.SkillGem.DoesNotExist:
                        continue
                    except models.SkillGem.MultipleObjectsReturned:
                        print(f"multiple gems with name '{value}'")
                        break

        if tag == 'td':
            if self.first_gem_reached:
                if self.classes[self.class_index] != 'Scion':
                    self.class_index += 1


class POEQuestWikiImporter(HTMLParser):
    '''Imports quest information from poewiki.net'''

    data = {
        'quests': []
    }
    next_a_is_quest = False
    last_quest_name = 'Atlas of Worlds'
    last_quest_reached = False
    current_act = 'Act_1'

    def handle_starttag(self, tag, attrs):
        '''Handle every new tag'''
        if tag == 'li':
            self.next_a_is_quest = True
        elif tag == 'a':
            title = ""
            url = ""
            is_quest = False
            if self.next_a_is_quest:
                self.next_a_is_quest = False
                for key, value in attrs:
                    if key == 'title':
                        title = value
                    if key == 'href':
                        if '/wiki/' in value:
                            is_quest = True
                            url = value
            if is_quest and not self.last_quest_reached:
                self.data['quests'].append({'title': title, 'act': self.current_act, 'url': url})
                if title == self.last_quest_name:
                    self.last_quest_reached = True
        elif tag == 'span':
            is_act = False
            for key, value in attrs:
                if key == 'class' and value == 'mw-headline':
                    is_act = True
                if is_act and key =='id' and 'Act_' in value:
                    self.current_act = value
        else:
            self.next_a_is_quest = False


class Job(DailyJob):
    '''Job'''
    help = "Daily Wiki Import for Quests"

    def execute(self):
        self.clear()
        self.gem_import()
        self.quest_import()
      
    def clear(self):
        '''clear all data'''
        print('deleting data')
        models.Quest.objects.all().delete()
        models.SkillGem.objects.all().delete()
        models.QuestRewardMapping.objects.all().delete()

    def quest_import(self):
        # QUEST IMPORT
        print('importing quests')
        r_quests = requests.get('https://www.poewiki.net/wiki/Quest')
        parser = POEQuestWikiImporter()
        parser.feed(r_quests.text)

        for quest in parser.data['quests']:
            quest_object = models.Quest()
            quest_object.title = quest['title']
            quest_object.act = quest['act']
            quest_object.url = quest['url']
            quest_object.save()

            # Map gem rewards
            reward_parser = POEQuestRewardWikiImporter()
            reward_parser.quest = quest_object
            r_rewards = requests.get(f"https://poewiki.net{quest_object.url}")
            reward_parser.feed(r_rewards.text)


    def gem_import(self):
        ''' Import skillgems'''
        print('importing gems')
        r_supports = requests.get('https://www.poewiki.net/wiki/Support_gem')
        r_skills = requests.get('https://www.poewiki.net/wiki/List_of_skill_gems')
        parser = POESkillGemWikiImporter()
        parser.feed(r_supports.text)
        
        parser = POESkillGemWikiImporter()
        parser.feed(r_skills.text)

        for entry in parser.data['gems']:
            gem = models.SkillGem()
            gem.name = entry['name']
            gem.save()


#    r_quests = requests.get('https://www.poewiki.net/wiki/The_Siren%27s_Cadence')
#    parser = POEQuestRewardWikiImporter()
#    parser.quest = models.Quest.objects.get(id=1)
#    parser.feed(r_quests.text)
