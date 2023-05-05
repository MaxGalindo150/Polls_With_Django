import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_publiseh_recently_with_future_questions(self):
        """was_published_recently returns False for question whose whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text = "Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)