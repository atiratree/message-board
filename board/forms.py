from django import forms

class MessageForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
		attrs={'placeholder': 'Title', 'class': 'textinput'}), max_length=70)
    content = forms.CharField(label='', widget=forms.TextInput(
		attrs={'placeholder': 'Message content', 'class': 'textinput'}), max_length=500)
	
class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=64)
	password = forms.CharField(widget=forms.PasswordInput())
	
class RegisterForm(forms.Form):
	username = forms.CharField(label='Username', max_length=64)
	password = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())
