from django.db import models
from users.models import Student, Teacher

class Sentence(models.Model):
    raw = models.CharField(max_length=400)
    diacritized = models.CharField(max_length=400, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_diacritized = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    diacritizer = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.raw

class SentenceAnswers(models.Model):
    model = models.CharField(max_length=24)
    text = models.CharField(max_length=400)
    sentence = models.ForeignKey(Sentence, on_delete=models.DO_NOTHING, related_name='sentence_answers')
