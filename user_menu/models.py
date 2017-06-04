from django.db import models

# Create your models here.


class UserTakings(models.Model):
    user_id = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return '[%s] %s: %s' % (self.user_id, self.date, self.description)

    def __repr__(self):
        return '[%s] %s: %s' % (self.user_id, self.date, self.description)
