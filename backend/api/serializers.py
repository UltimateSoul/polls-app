"""This module serves as serializer customizer"""

from rest_framework import serializers

from api.models import Poll, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""

    class Meta:
        model = Choice
        fields = ['message', 'votes']


class PollSerializer(serializers.ModelSerializer):
    """Poll's serializer"""

    choices = serializers.SerializerMethodField()

    def get_choices(self, poll):
        choices = poll.choices.all()
        serializer = ChoiceSerializer(choices, many=True, context={'request': self.context.get('request')})
        return serializer.data

    class Meta:
        model = Poll
        fields = ['question', 'choices']
