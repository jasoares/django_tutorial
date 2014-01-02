"""
Module responsible for storing poll information, including each poll
voting option, namely, choices and their relationships.
"""
import datetime
from django.db import models
from django.utils import timezone

class Poll(models.Model):
    """
    A Poll describes a vote between many options, which are called choices and
    included on each poll
    """
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """
        Returns true or false wether the poll was published somewhere
        in the last 24 hours
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    """
    A Choice describes a Poll vote option and has one and only one poll
    associated with it.
    """
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
