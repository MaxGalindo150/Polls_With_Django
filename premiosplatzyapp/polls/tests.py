import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_publiseh_recently_with_future_questions(self):
        """was_published_recently returns False for question whose whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text = "Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_publiseh_recently_with_past_questions(self):
        """was_published_recently returns False for question whose whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text = "Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_publiseh_recently_with_present_questions(self):
        """was_published_recently returns False for question whose whose pub_date is in the future"""
        time = timezone.now()
        future_question = Question(question_text = "Quién es el mejor Course Director de Platzi?",pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

def create_question(question_text, days):
    """This function creates a question. the parameters are the text of the question, and "days" is the number of days from the present to the day in which the question will be publicated"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date= time)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_future_questions_are_displayed(self):
        """If pub_date of a question is in the future, the question does not must be displayed"""
        create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_past_questions_are_displayed(self):
        """If pub_date of a question is in the past, the question has to be displayed"""
        question = create_question("Past question", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """
        past_question = create_question("Past question", -30)
        future_question = create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_question(self):
        """The question in the page may display multiple question"""
        past_question1 = create_question("Past question", -30)
        past_question2 = create_question("Past1 question", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question2, past_question1]
        )

    def test_two_future_question(self):
        """The question in the page may display multiple question"""
        future_question1 = create_question("Future question", 30)
        future_question2 = create_question("Future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in te future
        returns a 404 error not found
        """
        future_question = create_question("Future question", 30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past 
        displays the question's text
        """
        past_question = create_question("Past question", -30)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class ResultViewTest(TestCase):
    
    def test_results_of_future_questions_arent_displayed(self):
        """The results of a future question should not be displayed"""
        future_question = create_question("Future question", 30)
        url = reverse("polls:results", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_results_of_past_questions_are_displayed(self):
        """The results of past questions should be displayed"""
        past_question = create_question("Past question", -30)
        url = reverse("polls:results", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)