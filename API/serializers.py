from rest_framework import serializers
from .models import Sentence


class NewSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'urgent']


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent']

