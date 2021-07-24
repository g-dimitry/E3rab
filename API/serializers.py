from rest_framework import serializers
from .models import Sentence, SentenceAnswers
from users import serializers as otherSerializers

class NewSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'urgent']

class SentenceAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentenceAnswers
        fields = ['model', 'text']

class SentenceWithAnswersSerializer(serializers.ModelSerializer):
    author = otherSerializers.StudentSerializer(many=False, read_only=True)
    sentence_answers = SentenceAnswersSerializer(many=True, read_only=True)
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent', 'sentence_answers']

class SentenceSerializer(serializers.ModelSerializer):
    author = otherSerializers.StudentSerializer(many=False, read_only=True)
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent']

class OtherSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'date_diacritized', 'author','diacritizer', 'urgent']

