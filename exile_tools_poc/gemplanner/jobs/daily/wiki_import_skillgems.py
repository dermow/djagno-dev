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
                        self.data['gems'].append({'name': value})

class Job(DailyJob):
    '''Job'''
    help = "Daily Wiki Import for Skillgems"

    def execute(self):
        r_supports = requests.get('https://www.poewiki.net/wiki/Support_gem')
        r_skills = requests.get('https://www.poewiki.net/wiki/List_of_skill_gems')
        parser = POESkillGemWikiImporter()
        parser.feed(r_supports.text)
        parser.feed(r_skills.text)

        for entry in parser.data['gems']:
            gem = models.SkillGem()
            gem.name = entry['name']
            gem.save()
