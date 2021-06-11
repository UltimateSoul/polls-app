import factory

from api.models import Choice, Poll


class PollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Poll

    question = 'What\'s your favorite book?'


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Choice

    message = 'Eragon'
