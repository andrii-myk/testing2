from django.test import TestCase, Client
from django.urls import reverse
from testing.models import Question


class TestViews(TestCase):
    """ In this file django unit test has been used"""
    @classmethod
    def setUpTestData(cls):
        cls.question1 = Question.objects.create(
            question='Third planet from the Sun?'
        )
        cls.question2 = Question.objects.create(
            question='What?'
        )

    def setUp(self):
        self.client = Client()
        self.tests_index = reverse('testing:tests_index')
        self.questions_url = reverse('testing:questions_url')

    def test_index_GET(self):

        response = self.client.get(self.tests_index)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testing/index.html')

    def test_question_view_GET(self):
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testing/questions/questions.html')

    def test_question_create_POST(self):
        url = reverse('testing:question_create_url')
        response = self.client.post(url, {
            'question': 'Capital of Brazil?',
        })
        q1 = Question.objects.get(pk=1)
        q2 = Question.objects.get(pk=2)
        question = Question.objects.get(pk=3)
        self.assertEqual(question.question, 'Capital of Brazil?')
        self.assertEqual(q1.question, 'Third planet from the Sun?')
        self.assertEqual(q2.question, 'What?')
