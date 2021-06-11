from django.db import models


class Poll(models.Model):
    """This model represents Poll itself"""

    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_votes(self):
        return self.votes.all().count()  # noqa related connection

    def __str__(self):
        return self.question


class Choice(models.Model):
    """This model represents choice"""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    message = models.CharField(max_length=255)

    @property
    def total_votes(self):
        return self.choice_votes.all().count()  # noqa related connection

    def __str__(self):
        return self.message


class Vote(models.Model):
    """This model represents Vote for Choice

        This model contain poll foreign key in order to make available functionality of voting in multiple answers
        in one poll, that kind of functionality could be situated here: api/views/PollViewSet vote action method
        This model contain choice foreign key in order to determine which particular choice user did
    """

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes', blank=True, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choice_votes', blank=True, null=True)
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ['choice', 'ip_address']
