from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django import forms

from .models import Test, Question, TestRunAnswer, TestRun
from .forms import QuestionForm, TestForm, TestRunAnswerForm

# Create your views here.
def index(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        tests = Test.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        tests = Test.objects.all()
    

    return render(request, 'testing/index.html', context={'tests': tests})


class TestDetail(ListView):
    def get(self, request, slug):
        test = get_object_or_404(Test, slug__iexact=slug)
        return render(request, 'testing/tests/test_detail.html', context={'test': test})

class QuestionsView(ListView):
    def get(self, request):
        questions = Question.objects.all()
        return render(request, 'testing/questions/questions.html', context={'questions': questions})


class QuestionCreate(ListView):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'testing/questions/question_create.html', context={'form': form})

    def post(self, request):
        bound_form = QuestionForm(request.POST)
        if bound_form.is_valid:
            new_question = bound_form.save()
            return redirect(reverse('testing:questions_url'))
        return render(request, 'testing/questions/question_create.html', context={'form': bound_form})

class QuestionUpdate(ListView):
    def get(self, request, id):
        question = Question.objects.get(id__exact = id)
        bound_form = QuestionForm(instance=question)
        return render(request, 'testing/questions/question_update.html', context={'form': bound_form, 'question': question,})

    def post(self, request, id):
        question = Question.objects.get(id__exact = id)
        bound_form = QuestionForm(request.POST, instance=question)

        if bound_form.is_valid():
            updated_question = bound_form.save()
            return redirect(reverse('testing:questions_url'))
        return render(request, 'testing/questions/question_update.html', context={'form': bound_form, 'question': question})


class QuestionDelete(ListView):
    def get(self, request, id):
        question = Question.objects.get(id__exact = id)
        return render(request, 'testing/questions/question_delete.html', context={'question': question})

    def post(self, request, id):
        question = Question.objects.get(id__exact = id)
        question.delete()
        return redirect(reverse('testing:questions_url'))


class TestCreate(ListView):
    def get(self, request):
        form = TestForm()
        return render(request, 'testing/tests/test_create.html', context={'form': form})

    def post(self, request):
        bound_form = TestForm(request.POST)
        if bound_form.is_valid():
            new_test = bound_form.save()
            return redirect(reverse('testing:tests_index'))
        return render(request, 'testing/tests/test_create.html', context={'form': bound_form})


class TestUpdate(ListView):
    def get(self, request, id):
        test = Test.objects.get(id__exact = id)
        bound_form = TestForm(instance=test)
        return render(request, 'testing/tests/test_update.html', context={'form': bound_form, 'test': test,})

    def post(self, request, id):
        test = Test.objects.get(id__exact = id)
        bound_form = TestForm(request.POST, instance=test)

        if bound_form.is_valid():
            updated_test = bound_form.save()
            return redirect(reverse('testing:test_detail_url', kwargs={'slug': updated_test.slug}))
        return render(request, 'testing/tests/test_update.html', context={'form': bound_form, 'test': test})


class TestDelete(ListView):
    def get(self, request, id):
        test = Test.objects.get(id__exact = id)
        return render(request, 'testing/tests/test_delete.html', context={'test': test})

    def post(self, request, id):
        test = Test.objects.get(id__exact = id)
        test.delete()
        return redirect(reverse('testing:tests_index'))


class TestRunAnswerView(ListView):
    def get (self, request, id):
        TestRunFormSet = inlineformset_factory(TestRun, TestRunAnswer,fields=('question', 'answer'), exclude=('test_run', 'test_id'),
                        widgets={'question': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
                                 'answer': forms.TextInput(attrs={'class': 'form-control'})},
                                 extra=0)
        test = get_object_or_404(Test, pk=id)
        # instance = TestRun.objects.create(test=test)
        formset = TestRunFormSet(instance = test, queryset=TestRun.objects.filter(test__id=id))
        print(formset)
        return render(request, 'testing/tests/test_run.html', context={'formset': formset})

    # def post(self, request, id):
    #     TestRunFormSet = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), 
    #                     widgets={'question': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
    #                              'answer': forms.TextInput(attrs={'class': 'form-control'})},
    #                              extra=0)
    #     formset = TestRunFormSet(request.POST, queryset=Question.objects.filter(tests__id=id))
    #     print(formset)
    #     test_run = TestRun.objects.create(test=Test.objects.get(pk=id))

    #     form.fields['test_run'].choices = [(test_run, test_run)]

    #     if formset.is_valid():
    #         print('valid')
    #         return redirect(reverse('testing:tests_index'))
    #     return render(request, 'testing/tests/test_run.html', context={'formset': formset, 'id': id})


    
    # def get(self, request, id):
    #     test_run_set = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), form=TestRunAnswerForm, extra=0 )
    #     form = test_run_set(queryset=Test.objects.get(pk=id).questions.filter(tests__id=id))
    #     return render(request, 'testing/tests/test_run.html', context={'formset': form})
        
    # def get(self, request, id):
    #     test = get_object_or_404(Test, id=id)
    #     # test_run = TestRun.objects.create(test=test)

    #     formset = TestRunFormset(instance=test)
    #     return render(request, 'testing/tests/test_run.html', context={'formset': formset})
        
    # def post(self, request, id):

    #     test = get_object_or_404(Test, id=id)
    #     test_run = TestRun.objects.create(test=test)

    #     formset = TestRunFormset(instance=test_run, queryset=Question.objects.filter(tests__id=id))
    #     if formset.is_valid():
    #         formset.save()
    #         return redirect('tests_index')
    #     else:
    #         formset = TestRunFormset(instance=test)

    #     return render(request, 'testing/tests/test_run.html',context={
    #                 'test_run':test_run,
    #                 'formset':formset})

    # def post(self, request, id):
    #     test_run_set = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), form=TestRunAnswerForm, extra=0 )
    #     bound_formset = test_run_set(request.POST, queryset=Test.objects.get(pk=id).questions.filter(tests__id=id))
        


    #     if bound_formset.is_valid():
    #         instances = bound_formset.save(commit=False)
    #         for instance in instances:
    #             instance.save()
    #         return redirect(reverse('testing:index'))
    #     return render(request, 'testing/tests/test_run.html', context={'formset': bound_formset, 'id': id})