from django import forms

class MyForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class SimpleGemList(forms.Form):
    gem_list = forms.CharField(label='Gems')

class PasteBinForm(forms.Form):
    pastebin_url = forms.URLField(label='Pastebin URL')