from rest_framework import serializers
from .models import Sentence
from users import serializers as otherSerializers

class NewSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'urgent']


class SentenceSerializer(serializers.ModelSerializer):
    author = otherSerializers.StudentSerializer(many=False, read_only=True)
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent']

class OtherSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent']

