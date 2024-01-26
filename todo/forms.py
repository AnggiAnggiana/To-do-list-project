from django import forms
from django.forms import ModelForm
from .models import Regular_todo_list
from .models import Urgent_todo_list
from .models import Completed_todo_list

class Regular_todoForm(ModelForm):
    class Meta:
        model = Regular_todo_list
        fields = ('task', 'frequency', 'completed', 'author')
        labels = {
            'task': '',
            'frequency': '',
            'completed': '',
            'author': '',
        }
        
        # Styling form
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your task here'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'btn btn-success', 'input_type': 'button'}),
        }
        
    frequency = forms.ChoiceField(choices=Regular_todo_list.FREQUENCY_LEVEL)
    
    def __init__(self, *args, **kwargs):
        super(Regular_todoForm, self).__init__(*args, **kwargs)
        self.fields['author'].required = False
        
    def save(self, commit=True, user=None):
        instance = super(Regular_todoForm, self).save(commit=False)
        if not instance.author_id and user:
            instance.author = user
        if commit:
            instance.save()
        return instance
    
class Urgent_todoForm(ModelForm):
    class Meta:
        model = Urgent_todo_list
        fields = (('task', 'due_date', 'completed', 'author'))
        labels = {
            'task': '',
            'due_date': 'Deadline',
            'completed': '',
            'author': '',
        }
        
        # Styling form
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your task here'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Select deadline'}),
            'completed': forms.CheckboxInput(attrs={'class': 'btn btn-success', 'input_type': 'button'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Urgent_todoForm, self).__init__(*args, **kwargs)
        self.fields['author'].required = False
        
    def save(self, commit=True, user=None):
        instance = super(Urgent_todoForm, self).save(commit=False)
        if not instance.author_id and user:
            instance.author = user
        if commit:
            instance.save()
        return instance
        
class Completed_todoForm(ModelForm):
    regular_task = forms.ModelChoiceField(queryset=Regular_todo_list.objects.filter(completed=True), widget=forms.Select(attrs={'class': 'form-select'}))
    urgent_task = forms.ModelChoiceField(queryset=Urgent_todo_list.objects.filter(completed=True), widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Completed_todo_list
        fields = ('regular_task', 'urgent_task', 'author')
        labels = {
            'regular_task': 'Completed Regular Todo List',
            'urgent_task': 'Completed Urgent Todo List',
            'author': '',
        }
        
        # Styling Form
        widgets = {
            'regular_task': forms.Select(attrs={'class': 'form-select'}),
            'urgent_task': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Completed_todoForm, self).__init__(*args, **kwargs)
        self.fields['author'].required = False
        
    def save(self, commit=True, user=None):
        instance = super(Completed_todoForm, self).save(commit=False)
        if not instance.author_id and user:
            instance.author = user
        if commit:
            instance.save()
        return instance

from django import forms
from django.forms import ModelForm
from .models import Regular_todo_list
from .models import Urgent_todo_list
from .models import Completed_todo_list

class Regular_todoForm(ModelForm):
    class Meta:
        model = Regular_todo_list
        fields = ('task', 'frequency', 'completed')
        labels = {
            'task': '',
            'frequency': '',
            'completed': '',
        }
        
        # Styling form
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your task here'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'btn btn-success', 'input_type': 'button'}),
        }
        
    frequency = forms.ChoiceField(choices=Regular_todo_list.FREQUENCY_LEVEL)
    
class Urgent_todoForm(ModelForm):
    class Meta:
        model = Urgent_todo_list
        fields = (('task', 'due_date', 'completed'))
        labels = {
            'task': '',
            'due_date': 'Deadline',
            'completed': '',
        }
        
        # Styling form
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your task here'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Select deadline'}),
            'completed': forms.CheckboxInput(attrs={'class': 'btn btn-success', 'input_type': 'button'}),
        }
        
class Completed_todoForm(ModelForm):
    regular_task = forms.ModelChoiceField(queryset=Regular_todo_list.objects.filter(completed=True), widget=forms.Select(attrs={'class': 'form-select'}))
    urgent_task = forms.ModelChoiceField(queryset=Urgent_todo_list.objects.filter(completed=True), widget=forms.Select(attrs={'class': 'form-select'}))
    
    class Meta:
        model = Completed_todo_list
        fields = ('regular_task', 'urgent_task')
        labels = {
            'regular_task': 'Completed Regular Todo List',
            'urgent_task': 'Completed Urgent Todo List',
        }
        
        # Styling Form
        widgets = {
            'regular_task': forms.Select(attrs={'class': 'form-select'}),
            'urgent_task': forms.Select(attrs={'class': 'form-select'}),
        }