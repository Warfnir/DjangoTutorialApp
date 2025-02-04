import datetime

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_recent_question(self):
        time = timezone.now()
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)


def create_question(question_text, days):
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
       create_question(question_text="Past question.", days=-30)
       response = self.client.get(reverse('polls:index'))
       self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_future_question(self):
        create_question("Future question.",30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_and_past_questions(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 1.>','<Question: Past question 2.>'])
