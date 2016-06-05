from django import forms
from django.forms import SelectDateWidget

class MessageForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
		attrs={'placeholder': ' Title', 'class': 'textinput'}), max_length=70)
    content = forms.CharField(label='', widget=forms.TextInput(
		attrs={'placeholder': ' Message content', 'class': 'textinput'}), max_length=500)
	
class LoginForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(
		attrs={'placeholder': '', 'class': 'textinput'}), max_length=64)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'textinput'}))
	
class RegisterForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(
		attrs={'class': 'textinput'}), max_length=64)
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'textinput'}))
	password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'textinput'}))

class SearchForm(forms.Form):
	search = forms.CharField(required=False, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Search', 'class': 'textinput-search'}), max_length=50)
	searchAuthor = forms.CharField(required=False, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Search author', 'class': 'textinput-search'}), max_length=20)
	searchDate = forms.DateField(required=False, label='', widget=SelectDateWidget(
        empty_label=("Year", "Month", "Day")))