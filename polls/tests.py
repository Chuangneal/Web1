
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *


class TestAttendee(TestCase):

    def test_set_status(self):
        test_attendee = Attendee(email='test@mail.uic.edu.cn')
        test_attendee.set_status()
        self.assertIs(test_attendee.vote_status, 1)


class TestProgrammeJudge(TestCase):

    def test_finish_rating(self):
        test_programme_judge = ProgrammeJudge(password='000000', position='programme_judge', programme='test')
        test_programme_judge.finish_rating()
        self.assertIs(test_programme_judge.score_status, 1)


class TestHeadJudge(TestCase):

    def test_finish_rating(self):
        test_head_judge = HeadJudge(password='000000', position='head_judge', division='test')
        test_head_judge.finish_rating()
        self.assertIs(test_head_judge.score_status, 1)


class TestPoster(TestCase):

    # Threshold here is 1 week, there are 4 boundaries

    def test_was_published_recently_history_poster(self):
        # History time
        time = timezone.now() - datetime.timedelta(weeks=1.1)
        test_poster = Poster(pub_date=time, title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        self.assertIs(test_poster.was_generated_recently(), False)

    def test_was_published_recently_current_poster_1(self):
        # History time
        time = timezone.now() - datetime.timedelta(weeks=0.9)
        test_poster = Poster(pub_date=time, title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        self.assertIs(test_poster.was_generated_recently(), True)

    def test_was_published_recently_current_poster_2(self):
        # History time
        time = timezone.now() - datetime.timedelta(weeks=0.1)
        test_poster = Poster(pub_date=time, title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        self.assertIs(test_poster.was_generated_recently(), True)

    def test_was_published_recently_future_poster(self):
        # History time
        time = timezone.now() + datetime.timedelta(weeks=0.1)
        test_poster = Poster(pub_date=time, title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        self.assertIs(test_poster.was_generated_recently(), False)

    def test_increase_vote_amount(self):
        test_poster = Poster(title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        test_poster.increase_vote_amount()
        self.assertIs(test_poster.votes, 1)

    def test_increase_rate_amount(self):
        test_poster = Poster(title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        test_poster.increase_rate_amount(80)
        self.assertIs(test_poster.total_rate, 80)

    def test_increase_ticket_amount(self):
        test_poster = Poster(title='Test', author='Tester', programme='TestProgramme',
                             division='TestDivision', abstract="Testing", file_name='TestPoster.jpg', file_path='Test')
        test_poster.increase_ticket_amount(80)
        self.assertIs(test_poster.total_ticket, 80)


class TestEmailHistory(TestCase):

    # Threshold here is 5 minutes, there are 4 boundaries

    def test_was_published_recently_history_email_history(self):
        # History time
        time = timezone.now() - datetime.timedelta(minutes=5.1)
        history_email = EmailHistory(email='test@mail.uic.edu.cn', code='000000', send_date=time)
        self.assertIs(history_email.was_generated_recently(), False)

    def test_was_published_recently_current_email_history_1(self):
        # History time
        time = timezone.now() - datetime.timedelta(minutes=4.9)
        history_email = EmailHistory(email='test@mail.uic.edu.cn', code='000000', send_date=time)
        self.assertIs(history_email.was_generated_recently(), True)

    def test_was_published_recently_current_email_history_2(self):
        # History time
        time = timezone.now() - datetime.timedelta(minutes=0.1)
        history_email = EmailHistory(email='test@mail.uic.edu.cn', code='000000', send_date=time)
        self.assertIs(history_email.was_generated_recently(), True)

    def test_was_published_recently_future_email_history(self):
        # History time
        time = timezone.now() + datetime.timedelta(minutes=0.1)
        history_email = EmailHistory(email='test@mail.uic.edu.cn', code='000000', send_date=time)
        self.assertIs(history_email.was_generated_recently(), False)


# ------------- Previous work ------------- #

class TestQuestion(TestCase):

    # Threshold here is 1 day

    def test_was_published_recently_history_question(self):
        # History time
        time = timezone.now() - datetime.timedelta(days=2)
        history_question = Question(pub_date=time)
        self.assertIs(history_question.was_published_recently(), False)

    def test_was_published_recently_recently_question(self):
        # History time
        time = timezone.now() - datetime.timedelta(hours=12)
        history_question = Question(pub_date=time)
        self.assertIs(history_question.was_published_recently(), True)

    def test_was_published_recently_future_question(self):
        # Future time
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


