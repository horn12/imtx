from django import forms

class CommentForm(forms.Form):
#    author = forms.CharField(widget=forms.TextInput(attrs = {'onBlur': 'checkUser()'}))
    author = forms.CharField()
    email = forms.EmailField()
    url = forms.URLField(required = False)
    content = forms.CharField(widget=forms.Textarea(attrs = {'rows': '10', 'id': 'comment'}))
