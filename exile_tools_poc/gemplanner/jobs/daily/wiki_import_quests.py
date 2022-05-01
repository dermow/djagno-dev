from operator import is_
from django_extensions.management.jobs import DailyJob
from html.parser import HTMLParser
import requests
from gemplanner import models

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
            is_quest = False
            if self.next_a_is_quest:
                self.next_a_is_quest = False
                for key, value in attrs:
                    if key == 'title':
                        title = value
                    if key == 'href':
                        if '/wiki/' in value:
                            is_quest = True
            if is_quest and not self.last_quest_reached:
                self.data['quests'].append({'title': title, 'act': self.current_act})
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
        r_quests = requests.get('https://www.poewiki.net/wiki/Quest')
        parser = POEQuestWikiImporter()
        parser.feed(r_quests.text)

        for quest in parser.data['quests']:
            quest_object = models.Quest()
            quest_object.title = quest['title']
            quest_object.act = quest['act']
            quest_object.save()
