from __future__ import unicode_literals

from django.db import models

from django.conf import settings

# Create your models here.
class reminders(models.Model):
    receiverid = models.IntegerField()
    remindertime = models.CharField(max_length=50)
    reminder = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.receiverid
