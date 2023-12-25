import datetime
import secrets

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def user_can_vote(self, user) -> bool:
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(question=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()
    
    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success', 'danger', 'dark', 'warning', 'info']
            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count / self.get_vote_count)*100

            res.append(d)

        return res

    @admin.display(
            boolean=True,
            ordering='pub_date',
            description='Published recently',
    )
    def was_published_recently(self) -> bool:
        """
        Return True if the question has been published within the last day.
        Retrun False if the question has been published older than 1 day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self) -> str:
        return f"{self.question_text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self) -> str:
        return f'{self.question} - {self.choice_text}'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.question.question_text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
