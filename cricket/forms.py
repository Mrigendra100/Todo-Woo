from django import forms

class NameForm(forms.Form):
    player_name = forms.CharField(label='player name', max_length=100)