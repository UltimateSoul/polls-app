from django.db import models

from api.mixins import CreatedUpdatedAtMixin


class Poll(CreatedUpdatedAtMixin):
    """This model represents Poll itself"""

    question = models.TextField()

    @property
    def total_votes(self):
        total = 0
        for choice in self.choices:  # noqa related connection
            total += choice.choice_votes.count()
        return total

    def __str__(self):
        return self.question


class Choice(CreatedUpdatedAtMixin):
    """This model represents choice"""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    message = models.CharField(max_length=255)

    @property
    def total_votes(self):
        return self.choice_votes.all().count()  # noqa related connection

    def __str__(self):
        return self.message


class Vote(CreatedUpdatedAtMixin):
    """This model represents Vote for Choice

        This model contain poll foreign key in order to make available functionality of voting in multiple answers
        in one poll, that kind of functionality could be situated here: api/views/PollViewSet vote action method
        This model contain choice foreign key in order to determine which particular choice user did
    """

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choice_votes')
    ip_address = models.GenericIPAddressField()

    class Meta:
        unique_together = ['choice', 'ip_address']
