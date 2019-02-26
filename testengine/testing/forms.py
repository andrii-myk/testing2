from django import forms
from django.forms.models import BaseInlineFormSet 
from django.forms import inlineformset_factory
from .models import Question, Test, TestRun, TestRunAnswer

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
        widgets = {'question': forms.Select( attrs={'class': 'form-control', 'readonly':'readonly', 'disabled':'disabled'}),
                    'answer': forms.TextInput( attrs={'class': 'form-control', 'readonly':'readonly'})}

# class TestRunDetailForm(forms.Form):
#     question = forms.CharField(label="Question")
#     answer = forms.CharField(label="Answer")

# class BaseTestFormset(BaseInlineFormSet):

#     def add_fields(self, form, index):
#         super(BaseTestFormset, self).add_fields(form, index)

#         # save the formset in the 'nested' property
#         form.nested = TestRunAnswerForm(
#                         instance=form.instance,
#                         data=form.data if form.is_bound else None,
#                         files=form.files if form.is_bound else None,
#                         prefix='testrun-%s-%s' % (
#                             form.prefix,
#                             TestRunAnswerForm.get_default_prefix()),
#                         extra=0)
    
#     def is_valid(self):
#         result = super(BaseTestFormset, self).is_valid()

#         if self.is_bound:
#             for form in self.forms:
#                 if hasattr(form, 'nested'):
#                     result = result and form.nested.is_valid()

#         return result

#     def save(self, commit=True):

#         result = super(BaseTestFormset, self).save(commit=commit)

#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)

#         return result

# TestRunFormset = inlineformset_factory(TestRun,
#                                         TestRunAnswer,
#                                         formset=TestRunAnswerForm,
#                                         fields=('question', 'answer', 'test_run'))