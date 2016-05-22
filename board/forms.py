from django import forms

class MessageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=70)
    content = forms.CharField(label='Content', max_length=500)
