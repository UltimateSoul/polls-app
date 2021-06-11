"""This module serves as serializer customizer"""

from rest_framework import serializers

from api.models import Poll, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""

    class Meta:
        model = Choice
        fields = ['id', 'message', 'total_votes']


class VoteSerializer(serializers.ModelSerializer):
    """Create Votes Result Serializer"""

    class Meta:
        model = Vote
        fields = ['id', 'poll', 'choice']


class PollSerializer(serializers.ModelSerializer):
    """Listing Poll's objects serializer"""

    choices = ChoiceSerializer(many=True, required=False)
    results = VoteSerializer(many=True, read_only=True)

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
