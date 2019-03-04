from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.views.generic import ListView
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from .models import Test, Question, TestRunAnswer, TestRun
from .forms import QuestionForm, TestForm, TestRunAnswerForm, TestRunDetailForm
from notes.models import Note
from notes.forms import NoteForm


# Create your views here.
def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        tests = Test.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        tests = Test.objects.all()

    return render(request, 'testing/index.html', context={'tests': tests})


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
        question = Question.objects.get(id__exact=id)
        bound_form = QuestionForm(instance=question)
        return render(request, 'testing/questions/question_update.html', context={'form': bound_form, 'question': question, })

    def post(self, request, id):
        question = Question.objects.get(id__exact=id)
        bound_form = QuestionForm(request.POST, instance=question)

        if bound_form.is_valid():
            updated_question = bound_form.save()
            return redirect(reverse('testing:questions_url'))
        return render(request, 'testing/questions/question_update.html', context={'form': bound_form, 'question': question})


class QuestionDelete(ListView):
    def get(self, request, id):
        question = Question.objects.get(id__exact=id)
        return render(request, 'testing/questions/question_delete.html', context={'question': question})

    def post(self, request, id):
        question = Question.objects.get(id__exact=id)
        question.delete()
        return redirect(reverse('testing:questions_url'))


class TestDetail(ListView):
    def get(self, request, slug):
        test = get_object_or_404(Test, slug__iexact=slug)
        # content_type = ContentType.objects.get_for_model(test)
        # test_notes = Note.objects.filter(
        #     content_type__pk=content_type.pk,
        #     object_id=test.pk)
        # initital_data = {
        #     'content_type':content_type,
        #     'object_id': test.id,
        # }
        # note_form = NoteForm(request.Post or None, initial=initital_data)
        request.session['obj'] = {'object_id': test.id, 'model': 'test'}
        test_notes = Note.objects.filter_by_instance(test)
        return render(request, 'testing/tests/test_detail.html', context={'test': test, 'test_notes': test_notes, })


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
        test = Test.objects.get(id__exact=id)
        bound_form = TestForm(instance=test)
        return render(request, 'testing/tests/test_update.html', context={'form': bound_form, 'test': test})

    def post(self, request, id):
        test = Test.objects.get(id__exact=id)
        bound_form = TestForm(request.POST, instance=test)

        if bound_form.is_valid():
            updated_test = bound_form.save()
            return redirect(reverse('testing:test_detail_url', kwargs={'slug': updated_test.slug}))
        return render(request, 'testing/tests/test_update.html', context={'form': bound_form, 'test': test})


class TestDelete(ListView):
    def get(self, request, id):
        test = Test.objects.get(id__exact=id)
        return render(request, 'testing/tests/test_delete.html', context={'test': test})

    def post(self, request, id):
        test = Test.objects.get(id__exact=id)
        test.delete()
        return redirect(reverse('testing:tests_index'))


class TestRunAnswerView(ListView):
    def get(self, request, id):
        TestRunFormSet = modelformset_factory(TestRunAnswer, fields=('question', 'answer'), form=TestRunAnswerForm, extra=0)
        formset = TestRunFormSet(queryset=Test.objects.get(pk=id).questions.filter(tests__id=id))
        return render(request, 'testing/test_runs/test_run.html', context={'formset': formset})

    # WARNING BELOW YOU'RE GOING TO WATCH A LOT OF BAD CODE
    def post(self, request, id):
        questions = Question.objects.filter(tests__id=id)
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
            my_formset.append(TestRunDetailForm(instance=test_run_answer))
        content_type = ContentType.objects.get_for_model(test_run)
        print(content_type)
        request.session['obj'] = {'object_id': test_run.id, 'model': 'testrun'}
        test_run_notes = Note.objects.filter_by_instance(test_run)
        return render(request, 'testing/test_runs/test_run_detail.html', context={'formset': my_formset, 'test_run': test_run, 
                                                                                  'test_run_notes': test_run_notes})


class TestRunTestList(ListView):
    """Class for showing test_runs bounded to specific Test"""
    def get(self, request, id):
        test_runs = TestRun.objects.filter(test__id=id)
        return render(request, 'testing/test_runs/test_runs_test_list.html', context={'test_runs': test_runs})


class AddNoteView(ListView):
    def get(self, request):
        obj = request.session.get('obj', None)
        obj_id = obj['object_id']
        mod = obj['model']
        print(mod)
        print(obj_id)
        ct = ContentType.objects.get(app_label='testing', model=mod)
        print(ct)
        instance = ct.get_object_for_this_type(id=obj_id)
        initial_data = {
            'content_type': ct,
            'object_id': obj_id,
        }
        form = NoteForm(initial=initial_data)
        return render(request, 'notes/add_note.html', context={'form': form, 'instance': instance})

    def post(self, request):
        obj = request.session.get('obj', None)
        obj_id = obj['object_id']
        mod = obj['model']
        content_type = ContentType.objects.get(model=mod)
        # initial_data = {
        #     'content_type': content_type,
        #     'object_id': obj_id,
        # }

        form = NoteForm(request.POST)

        if form.is_valid():
            c_type = form.cleaned_data.get("content_type")
            obj_id = form.cleaned_data.get("object_id")
            text_data = form.cleaned_data.get("text")
            new_note = Note.objects.get_or_create(
                author=request.user,
                content_type=content_type,
                object_id=obj_id,
                text=text_data,
            )
            return redirect(reverse('notes:instance_notes_url'))
        return render(request, 'notes/add_note.html', context={'form': form})
