from django.views.generic import TemplateView
from rest_framework import viewsets

from api.models import Poll, Choice
from api.serializers import PollSerializer, ChoiceSerializer


class HomeView(TemplateView):
    template_name = 'api/home.html'


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}