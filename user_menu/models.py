from django.db import models
from django.utils.timezone import now

from wellbot.settings import DATETIME_FORMAT
# Create your models here.


class UserTakings(models.Model):
    user_id = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return '[%s] %s: %s' % (self.user_id, self.date, self.description)

    def __repr__(self):
        return '[%s] %s: %s' % (self.user_id, self.date, self.description)


class CorezoidState(models.Model):
    chat_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=1000)
    date = models.DateTimeField(default=now)
    timeout = models.IntegerField(default=0)
    context = models.TextField(default='')

    def __str__(self):
        return 'chat_id=%s, task_id=%s, date=%s, timeout=%s seconds, context=%s' % (self.chat_id, self.task_id, self.date.strptime(DATETIME_FORMAT), self.timeout, self.context)

    def __repr__(self):
        return 'chat_id=%s, task_id=%s, date=%s, timeout=%s seconds, context=%s' % (self.chat_id, self.task_id, self.date.strptime(DATETIME_FORMAT), self.timeout, self.context)


class CorezoidStateHistory(models.Model):
    chat_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=1000)
    date = models.DateTimeField(default=now)
    timeout = models.IntegerField(default=0)
    context = models.TextField(default='')

    def __str__(self):
        return 'chat_id=%s, task_id=%s, date=%s, timeout=%s seconds, context=%s' % (self.chat_id, self.task_id, self.date.strptime(DATETIME_FORMAT), self.timeout, self.context)

    def __repr__(self):
        return 'chat_id=%s, task_id=%s, date=%s, timeout=%s seconds, context=%s' % (self.chat_id, self.task_id, self.date.strptime(DATETIME_FORMAT), self.timeout, self.context)
