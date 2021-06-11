from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from api.models import Poll
from api.serializers import PollSerializer, ResultSerializer
from api.utils import get_client_ip


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_serializer_context(self, *args, **kwargs):  # noqa
        return {'request': self.request}

    @swagger_auto_schema(description="Create new poll", request_body=PollSerializer,
                         response={status.HTTP_201_CREATED: PollSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(description="Voting in polls", request_body=ResultSerializer,
                         response={status.HTTP_201_CREATED: ResultSerializer})
    @action(methods=['POST'], serializer_class=ResultSerializer, detail=False, url_name='vote', url_path='vote')
    def vote(self, request, *args, **kwargs):  # noqa
        serializer = ResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip_address = get_client_ip(self.request)
        poll = serializer.validated_data.get('poll')
        choice = serializer.validated_data.get('choice')
        ip_address_exists = poll.results.filter(ip_address=ip_address)
        if ip_address_exists:
            data = {"detail": "You have already voted!"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        choice_connected_to_poll = poll.choices.filter(id=choice.id).exists()
        if choice_connected_to_poll:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'Message': 'You\'ve voted successfully!'}, status=status.HTTP_201_CREATED, headers=headers)
        data = {"detail": 'This choice doesn\'t connected to poll itself!'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
