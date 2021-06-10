from django.views.generic import TemplateView
from rest_framework import viewsets

from api.models import Poll
from api.serializers import PollSerializer


class HomeView(TemplateView):
    template_name = 'api/home.html'


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

