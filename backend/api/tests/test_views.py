import json

from django.urls import reverse
from rest_framework.test import APITestCase

from api.tests.factories import PollFactory, ChoiceFactory


class TestProfileView(APITestCase):

    def setUp(self) -> None:
        self.poll = PollFactory()
        self.poll.save()
        self.choice = ChoiceFactory(poll=self.poll)
        self.choice.save()

    def test_poll_view_create_success(self):
        """Checks flow when user goes to his profile"""
        poll_response = self.client.get(reverse('api:polls-list'))
        self.assertTrue(poll_response.status_code == 200)
        response = json.loads(poll_response.content)[0]
        self.assertTrue(response.get('question') == self.poll.question)
        self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)
