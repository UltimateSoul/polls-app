from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.models import Poll, Choice
from api.serializers import PollSerializer, ChoiceSerializer, CreateResultSerializer
from api.utils import get_client_ip


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


class VoteUsers(CreateAPIView):
    """View to vote in polls"""

    serializer_class = CreateResultSerializer

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        """Modified in order to handle voting options per one IP address"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip_address = get_client_ip(self.request)
        ip_address_exists = serializer.validated_data.get('poll').results.filter(ip_address=ip_address)
        if ip_address_exists:
            data = {"detail": "You have already voted!"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'Message': 'You\'ve voted successfully!'}, status=status.HTTP_201_CREATED, headers=headers)
