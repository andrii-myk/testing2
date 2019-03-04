from django import forms
from django.forms.models import BaseInlineFormSet 
from django.forms import inlineformset_factory
from .models import Question, Test, TestRun, TestRunAnswer, Note


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question',]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ('slug',)
        fields = ['title', 'description', 'questions']
        queryset = Question.objects.all()
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'questions': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class TestRunAnswerForm(forms.ModelForm):
    class Meta:
        model = TestRunAnswer
        fields = ('question', 'answer')
        # exclude = ('test_run',)
        widgets = {'question': forms.TextInput( attrs={'class': 'form-control', 'readonly':'readonly'}),
                    'answer': forms.TextInput( attrs={'class': 'form-control'})}


class TestRunDetailForm(forms.ModelForm):
    class Meta:
        model = TestRunAnswer
        fields = ('question', 'answer')
        # # exclude = ('test_run',)
        widgets = {'question': forms.Select( attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'}),
                    'answer': forms.TextInput( attrs={'class': 'form-control', 'readonly': 'readonly'})}


# class NoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = ('text',)

#         widgets = {
#             'text': forms.TextInput(attrs={'class': 'form-control'})
#         }
