"""This module serves as serializer customizer"""

from rest_framework import serializers

from api.models import Poll, Choice, Result
from api.utils import get_client_ip


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""

    class Meta:
        model = Choice
        fields = ['id', 'message', 'total_votes']


class ResultSerializer(serializers.ModelSerializer):
    """Create Votes Result Serializer"""

    class Meta:
        model = Result
        fields = ['id', 'poll', 'choice']


class PollSerializer(serializers.ModelSerializer):
    """Listing Poll's objects serializer"""

    choices = ChoiceSerializer(many=True, required=True)
    results = ResultSerializer(many=True, read_only=True)

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        instance = Poll.objects.create(**validated_data)
        for choice_data in choices:
            choice = Choice.objects.create(poll=instance, **choice_data)
            choice.save()
        return instance

    class Meta:
        model = Poll
        fields = ['id', 'question', 'choices', 'results']
