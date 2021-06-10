from django.db import models


class Poll(models.Model):
    """This model represents Poll itself"""

    question = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


# class UserMetaData(models.Model):
#     """This represents serves as place which contains user metadata such as User Agent, IP etc"""


class Choice(models.Model):
    """This model represents choice"""

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    message = models.CharField(max_length=255, null=True, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.message
