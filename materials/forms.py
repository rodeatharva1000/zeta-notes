from django import forms
from .models import Subject, Content

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class AddContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['file', 'image', 'description', 'subject']
        

class ChooseSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(), 
        empty_label="Select a Subject" 
    )
