from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from api.models import Poll
from api.serializers import PollSerializer, VoteSerializer
from api.utils import get_client_ip


vote_response = openapi.Response('You\'ve voted successfully!', VoteSerializer)


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

    @swagger_auto_schema(description="Voting in polls", request_body=VoteSerializer,
                         responses={status.HTTP_201_CREATED: vote_response,
                                    status.HTTP_400_BAD_REQUEST: "You have already voted!"})
    @action(methods=['POST'], serializer_class=VoteSerializer, detail=True, url_name='vote', url_path='vote')
    def vote(self, request, *args, **kwargs):  # noqa args and kwargs issues
        """Handles votes in polls"""

        serializer = VoteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        ip_address = get_client_ip(self.request)
        poll = Poll.objects.get(pk=kwargs.get('pk'))
        choice = serializer.validated_data.get('choice')
        ip_address_exists = poll.choices.filter(choice_votes__ip_address=ip_address).exists()

        if ip_address_exists:  # This functionality could be switched in order to make flexibility in multiple choices
            data = {"detail": "You have already voted!"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        choice_connected_to_poll = poll.choices.filter(id=choice.id).exists()
        if choice_connected_to_poll:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'Message': 'You\'ve voted successfully!'}, status=status.HTTP_201_CREATED, headers=headers)

        data = {"detail": 'The poll doesn\'t have this choice'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
