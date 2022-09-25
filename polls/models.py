
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Attendee(models.Model):
    objects = models.Manager()

    email = models.CharField(max_length=100)
    vote_status = models.IntegerField(default=0)

    def set_status(self):
        self.vote_status += 1
        self.save()


class Conference(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, default="CMS")
    conf_date = models.DateTimeField('Conference Start')
    abstract = models.CharField(max_length=1000, default="The organizers were lazy and left nothing.")

    # Judge number:
    programme_judge_num = models.IntegerField(default=2)
    head_judge_num = models.IntegerField(default=2)

    # Lucky draw:
    first_prize_num = models.IntegerField(default=0)
    second_prize_num = models.IntegerField(default=0)
    third_prize_num = models.IntegerField(default=0)


# --------- multi-table inheritance START --------- #

class Staff(models.Model):
    objects = models.Manager()

    password = models.CharField(max_length=10, default='000000')
    position = models.CharField(max_length=10, default='No position')


class ProgrammeJudge(Staff):

    programme = models.CharField(max_length=10, default='cst')
    score_status = models.IntegerField(default=0)

    def finish_rating(self):
        self.score_status = 1
        self.save()


class HeadJudge(Staff):

    division = models.CharField(max_length=10, default='dst')
    score_status = models.IntegerField(default=0)

    def finish_rating(self):
        self.score_status = 1
        self.save()


class Chairman(Staff):
    pass


class Coordinator(Staff):
    pass


class Admin(Staff):
    pass

# --------- multi-table inheritance END --------- #


# --------- multi-table inheritance Start --------- #

class Poster(models.Model):
    objects = models.Manager()

    # Basic info
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    programme = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    abstract = models.CharField(max_length=1000)

    # Vote info
    votes = models.IntegerField(default=0)

    # Rate info
    total_rate = models.IntegerField(default=0)  # the sum of rate
    number_rate = models.IntegerField(default=0)  # the number of judge who rates it
    total_ticket = models.IntegerField(default=0)  # the tickets received in the division
    number_ticket = models.IntegerField(default=0)  # the number of head judge who gives ticket

    # File info
    file_name = models.CharField(max_length=100)
    file_width = models.IntegerField(default=0)
    file_height = models.IntegerField(default=0)
    file_path = models.CharField(max_length=100)

    # Other info
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def increase_vote_amount(self):
        self.votes += 1
        self.save()

    # Regular Judge
    def increase_rate_amount(self, rate):
        self.total_rate += int(rate)
        self.number_rate += 1
        self.save()

    # Head Judge
    def increase_ticket_amount(self, ticket):
        self.total_ticket += int(ticket)
        self.number_ticket += 1
        self.save()

    def get_vote_amount(self):
        return self.votes

    def get_avg_rate(self):
        if self.number_rate != 0:
            return round(self.total_rate / self.number_rate, 2)
        else:
            return False

    def was_generated_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= timezone.now() - datetime.timedelta(weeks=1)


class EmailHistory(models.Model):
    objects = models.Manager()

    email = models.CharField(max_length=200)
    code = models.IntegerField()
    send_date = models.DateTimeField('date published', default=timezone.now)

    def was_generated_recently(self):
        now = timezone.now()
        return now >= self.send_date >= timezone.now() - datetime.timedelta(minutes=5)


class UICInfo(models.Model):
    object = models.Manager()

    division = models.CharField(max_length=200)
    programme = models.CharField(max_length=200)


class Question(models.Model):  # Here, we use .<foreignKey>_set.all()/.count() to get foreign set
    objects = models.Manager()

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # It's important -- for Django's automatically-generated admin
        return self.question_text

    @admin.display(  # Let be a small symbol
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    objects = models.Manager()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text