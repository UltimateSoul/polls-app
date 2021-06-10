"""This module serves as serializer customizer"""

from rest_framework import serializers

from api.models import Poll, Choice, Result
from api.utils import get_client_ip


class ChoiceSerializer(serializers.ModelSerializer):
    """Choice Serializer"""

    class Meta:
        model = Choice
        fields = ['id', 'message', 'total_votes']

    def update(self, instance, validated_data):
        ip_address = get_client_ip(self.context.get('request'))
        ip_exists = (instance.cresults.filter(ip_address=ip_address, ).
                     exists())  # Check if that user already voted or not
        instance.message = validated_data.get('message')
        if ip_exists:
            instance.save()
            return instance

        Result.objects.create(choice=instance, poll=instance.poll, ip_address=ip_address)  # Create new user IP
        instance.save()
        return instance


class CreateResultSerializer(serializers.ModelSerializer):
    """Votes Result Serializer"""

    class Meta:
        model = Result
        fields = ['id', 'poll', 'choice']

    def create(self, validated_data):
        ip_address = get_client_ip(self.context.get('request'))
        validated_data.update({'ip_address': ip_address})
        result = Result.objects.create(**validated_data)
        result.save()
        return result


class PollSerializer(serializers.ModelSerializer):
    """Listing Poll's objects serializer"""

    choices = serializers.SerializerMethodField()

    def get_choices(self, poll):
        choices = poll.choices.all()
        serializer = ChoiceSerializer(choices, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def create(self, validated_data):
        instance = Poll.objects.create(**validated_data)
        return instance

    class Meta:
        model = Poll
        fields = ['id', 'question', 'choices']
