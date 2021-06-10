from django.db import models


class Poll(models.Model):
    """This model represents Poll itself"""

    question = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_votes(self):
        return self.results.all().count()

    def __str__(self):
        return self.question


class Choice(models.Model):
    """This model represents choice"""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    message = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.message


class Result(models.Model):
    """This model represents Vote for Choice"""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='results', blank=True, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choice_results', blank=True, null=True)
    ip_address = models.CharField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        unique_together = ['choice', 'poll', 'ip_address']
