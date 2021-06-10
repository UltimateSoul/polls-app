from django.views.generic import TemplateView
from rest_framework import viewsets

from core.models import Poll
from core.serializers import PollSerializer


class HomeView(TemplateView):
    template_name = 'core/home.html'


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
