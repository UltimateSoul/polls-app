"""This module serves as serializer customizer"""

from rest_framework import serializers

from api.models import Poll, Choice, Vote
from api.utils import get_client_ip


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""

    class Meta:
        model = Choice
        fields = ['id', 'message', 'total_votes']


class VoteSerializer(serializers.ModelSerializer):
    """Create Votes Result Serializer"""

    class Meta:
        model = Vote
        fields = ['id', 'choice']

    def create(self, validated_data):
        self.context.get(f'REQUEST:   ', 'request')
        ip_address = get_client_ip(self.context.get('request'))
        validated_data.update({'ip_address': ip_address})
        vote = Vote.objects.create(**validated_data)
        vote.save()
        return vote


class PollSerializer(serializers.ModelSerializer):
    """Listing Poll's objects serializer"""

    total_votes = serializers.ReadOnlyField()
    choices = ChoiceSerializer(many=True, required=True)
    votes = VoteSerializer(many=True, read_only=True)

    def create(self, validated_data):

        choices = validated_data.pop('choices')
        instance = Poll.objects.create(**validated_data)
        for choice_data in choices:
            choice = Choice.objects.create(poll=instance, **choice_data)
            choice.save()
        return instance

    class Meta:
        model = Poll
        fields = ['id', 'question', 'choices', 'votes', 'total_votes']
