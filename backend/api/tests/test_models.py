from rest_framework.test import APITestCase

from api.models import Poll, Choice
from api.tests.factories import PollFactory, ChoiceFactory


class TestModels(APITestCase):

    def test_creation_poll(self):
        poll = PollFactory()
        poll.save()
        choice = ChoiceFactory(poll=poll)
        choice.save()
        self.assertTrue(Poll.objects.exists())
        self.assertTrue(Choice.objects.exists())
