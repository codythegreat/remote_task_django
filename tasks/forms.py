from django import forms
from django.utils import timezone

class CreateTeamForm(forms.Form):
    name = forms.CharField(max_length=255)
    private = forms.BooleanField(initial=True, required=False   )

class JoinTeamForm(forms.Form):
    teamPrimKey = forms.IntegerField()

class CreateTaskForm(forms.Form):
    title = forms.CharField(max_length=255)
    desc = forms.CharField(max_length=512)
    endDate = forms.DateField() 

class CompleteTaskForm(forms.Form):
    taskId= forms.IntegerField()

class CommentOnTask(forms.Form):
    pass
