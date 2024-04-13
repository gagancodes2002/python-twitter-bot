from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = '__all__'


class TodoFilterForm(forms.Form):
    STATUS_CHOICES = (
        ('all', 'All'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)