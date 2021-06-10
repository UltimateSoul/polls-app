from rest_framework import serializers


# Serializers define the API representation.
from .models import Poll


class PollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = ['question']
