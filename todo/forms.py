from django import forms
from django.forms import ModelForm
from .models import Regular_todo_list
from .models import Urgent_todo_list

class Regular_todoForm(ModelForm):
    class Meta:
        model = Regular_todo_list
        fields = ('task', 'frequency', 'completed')
        labels = {
            'task': 'Regular Todo List',
            'frequency': 'Type',
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
            'task': 'Urgent Todo List',
            'due_date': 'Deadline',
            'completed': '',
        }
        
        # Styling form
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your task here'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Select deadline'}),
            'completed': forms.CheckboxInput(attrs={'class': 'btn btn-success', 'input_type': 'button'}),
        }