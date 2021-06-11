import json

from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Poll, Choice
from api.tests.factories import PollFactory, ChoiceFactory


class TestPollView(APITestCase):

    def setUp(self) -> None:
        self.poll = PollFactory()
        self.poll.save()
        self.choice = ChoiceFactory(poll=self.poll)
        self.choice.save()

    def test_poll_view_list_success(self):
        """Checks that polls can be listed successfully"""

        poll_response = self.client.get(reverse('api:polls-list'))
        self.assertTrue(poll_response.status_code == 200)
        response = json.loads(poll_response.content)[0]
        self.assertTrue(response.get('question') == self.poll.question)
        self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)

    def test_poll_view_retrieve_success(self):
        """Checks that poll can be retrieved"""

        params = {'pk': self.poll.id}
        poll_response = self.client.get(reverse('api:polls-detail', kwargs=params))
        self.assertTrue(poll_response.status_code == 200)
        response = json.loads(poll_response.content)
        self.assertTrue(response.get('question') == self.poll.question)
        self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)

    def test_poll_view_delete_success(self):
        """Checks that poll can be delete successfully"""

        params = {'pk': self.poll.id}
        poll_response = self.client.delete(reverse('api:polls-detail', kwargs=params))
        self.assertTrue(poll_response.status_code == 204)
        self.assertFalse(Poll.objects.all().exists())
        self.assertFalse(Choice.objects.all().exists())

    def test_poll_view_update_success(self):
        """Checks that poll can be updated successfully"""

        params = {'pk': self.poll.id}
        new_question = f"Updated old message: {self.poll.question}"
        data = {'question': new_question}
        poll_response = self.client.patch(reverse('api:polls-detail', kwargs=params), data)
        self.assertTrue(poll_response.status_code == 200)
        response = json.loads(poll_response.content)
        self.assertTrue(response.get('question') == new_question)

    # def test_create_poll_with_choices


    # def test_poll_view_list_success(self):
    #     """Checks flow when user goes to his profile"""
    #
    #     poll_response = self.client.get(reverse('api:polls-list'))
    #     self.assertTrue(poll_response.status_code == 200)
    #     response = json.loads(poll_response.content)[0]
    #     self.assertTrue(response.get('question') == self.poll.question)
    #     self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)

