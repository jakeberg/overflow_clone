from django import forms
from overflow_clone.models import Tag


class SignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class QuestionForm(forms.Form):
    body = forms.CharField(label='Question?', widget=forms.Textarea())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
        )


class AnswerForm(forms.Form):

    body = forms.CharField(label='Answer', widget=forms.Textarea())