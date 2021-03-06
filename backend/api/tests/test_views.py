import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Poll, Choice
from api.tests.factories import PollFactory, ChoiceFactory

IP_ADDRESSES = ['25.112.160.25',
                '89.131.217.251',
                '69.132.146.10',
                '190.115.63.68',
                '156.140.160.206']


class TestPollView(APITestCase):

    def setUp(self) -> None:
        self.poll = PollFactory()
        self.poll.save()
        self.choice = ChoiceFactory(poll=self.poll)
        self.choice.save()

    def test_poll_view_list_success(self):
        """Checks that polls can be listed successfully"""

        poll_response = self.client.get(reverse('api:polls-list'))
        self.assertTrue(poll_response.status_code == status.HTTP_200_OK)
        response = json.loads(poll_response.content)[0]
        self.assertTrue(response.get('question') == self.poll.question)
        self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)

    def test_poll_view_retrieve_success(self):
        """Checks that poll can be retrieved"""

        params = {'pk': self.poll.id}
        poll_response = self.client.get(reverse('api:polls-detail', kwargs=params))
        self.assertTrue(poll_response.status_code == status.HTTP_200_OK)
        response = json.loads(poll_response.content)
        self.assertTrue(response.get('question') == self.poll.question)
        self.assertTrue(response.get('choices')[0].get('message') == self.choice.message)

    def test_poll_view_delete_success(self):
        """Checks that poll can be delete successfully"""

        params = {'pk': self.poll.id}
        poll_response = self.client.delete(reverse('api:polls-detail', kwargs=params))
        self.assertTrue(poll_response.status_code == status.HTTP_204_NO_CONTENT)
        self.assertFalse(Poll.objects.all().exists())
        self.assertFalse(Choice.objects.all().exists())

    def test_poll_view_update_success(self):
        """Checks that poll can be updated successfully"""

        params = {'pk': self.poll.id}
        new_question = f"Updated old message: {self.poll.question}"
        data = {'question': new_question}
        poll_response = self.client.patch(reverse('api:polls-detail', kwargs=params), data)
        self.assertTrue(poll_response.status_code == status.HTTP_200_OK)
        response = json.loads(poll_response.content)
        self.assertTrue(response.get('question') == new_question)

    def test_create_poll_with_choices_success(self):
        data = {
            "question": "Do you like films?",
            "choices": [
                {
                    "message": "Yep"
                },
                {
                    "message": "No"
                },
                {
                    "message": "Don't know what to answer"
                },
                {
                    "message": "See testss"
                }
            ]
        }
        poll_response = self.client.post(reverse('api:polls-list'), json.dumps(data), content_type='application/json')
        self.assertEqual(poll_response.status_code, status.HTTP_201_CREATED)
        response = json.loads(poll_response.content)
        poll_id = response.get('id')
        self.assertTrue(Poll.objects.filter(id=poll_id).exists())
        for choice in response.get('choices'):
            self.assertTrue(Choice.objects.filter(id=choice.get('id')).exists())

    def test_vote_poll_on_choices_success(self):
        data = {
            "choice": self.choice.id
        }
        params = {'pk': self.poll.id}
        vote_response = self.client.post(reverse('api:polls-vote', kwargs=params), data)
        self.assertEqual(vote_response.status_code, status.HTTP_201_CREATED)

