from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Test, Question, TestRunAnswer, TestRun, Note
from .forms import QuestionForm, TestForm, TestRunAnswerForm, TestRunDetailForm, NoteForm

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
        content_type = ContentType.objects.get_for_model(test)
        test_notes = Note.objects.filter(
            content_type__pk=content_type.pk,
            object_id=test.pk)
        return render(request, 'testing/tests/test_detail.html', context={'test': test,'test_notes': test_notes})


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
    def get(self, request, id):
        TestRunFormSet = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), form=TestRunAnswerForm, extra=0 )
        formset = TestRunFormSet(queryset=Test.objects.get(pk=id).questions.filter(tests__id=id))
        return render(request, 'testing/test_runs/test_run.html', context={'formset': formset})
        
    #WARNING BELOW YOU'RE GOING TO WATCH A LOT OF BAD CODE
    def post(self, request, id):
        questions=Question.objects.filter(tests__id=id)
        TestRunFormSet = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), form=TestRunAnswerForm, extra=0)
        bound_formset = TestRunFormSet(request.POST, queryset=questions)
        answer_questions = {}
        answer_error = False
        for form in bound_formset.forms:
            form.is_valid()
            q_str = form['question'].data
            question = 's'
            for q in questions:
                if q.question == q_str:
                    question = q
            answer = form.cleaned_data.get('answer')
            if not answer or not question:
                answer_error = True
            answer_questions[question] = answer            
            
        if answer_error:
            return render(request, 'testing/test_runs/test_run.html', context={'formset': bound_formset, 'id': id})
        else:
            test_run = TestRun.objects.create(test=Test.objects.get(pk=id))
            for question, answer in answer_questions.items():
                TestRunAnswer.objects.create(question=question, answer=answer, test_run=test_run) 
            return redirect(reverse('testing:tests_index'))


class TestRuns(ListView):
    def get(self, request):
        test_runs = TestRun.objects.all()
        return render(request, 'testing/test_runs/test_runs_list.html', context={'test_runs': test_runs})


class TestRunDetail(ListView):
    def get(self, request, id):
        test_run = get_object_or_404(TestRun, pk=id)
        test_run_answers = TestRunAnswer.objects.filter(test_run__id=id)
        my_formset = []
        for test_run_answer in test_run_answers:
            print(dir(test_run_answer))
            print(test_run)
            my_formset.append(TestRunDetailForm(instance=test_run_answer))
        print(my_formset)
        return render(request, 'testing/test_runs/test_run_detail.html', context={'formset': my_formset, 'test_run':test_run})


class TestRunTestList(ListView):
    """Class for showing test_runs bounded to specific Test"""
    def get(self, request, id):
        test_runs = TestRun.objects.filter(test__id=id)
        return render(request, 'testing/test_runs/test_runs_test_list.html', context={'test_runs': test_runs})


class AddNoteView(ListView):
    def get(self, request):
        bound_form = NoteForm()
        return render(request, 'testing/notes/add_note.html', context={'form': bound_form})

    def post(self, request, *args, **kwargs):
        obj_pk = kwargs.get('pk')
        obj_type = kwargs.get('type')
        model = apps.get_model('testing', obj_type)
        instance = model.objects.get(pk=obj_pk)
        bound_form = NoteForm(request.Post, instance=instance)

        if bound_form.is_valid():
            note_form = bound_form.save()
            # instance.notes.create(author=request.user, text=)
            return redirect(reverse('testing:test_detail_url', kwargs={'slug': updated_test.slug}))
        return render(request, 'testing/notes/add_note.html', context={'form': bound_form, 'note': note_form})


# class NotesListView(ListView):
#     model = NoteItem
#     template_name = 'notes/notes.html'

#     def get_queryset(self):
#         model_type = self.kwargs['type']
#         content = ContentType.objects.get(model=model_type)
#     return self.model.objects.filter(content_type=content.id)