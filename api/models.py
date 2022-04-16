from django.db import models
from django.contrib.auth import get_user_model

from questionnaire.settings import QUESTION_TYPES

User = get_user_model()


class Questionnaire(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    date_start = models.DateField(auto_now_add=True, verbose_name='Start date')
    date_end = models.DateField(verbose_name='End date')
    description = models.CharField(max_length=200, verbose_name='Description')

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        verbose_name='Тип вопроса',
    )
    questionnaire = models.ForeignKey(
        Questionnaire, blank=True, on_delete=models.CASCADE,
        related_name="questions"
    )

    def __str__(self):
        return self.text


class Choice(models.Model):
    name = models.TextField(verbose_name='Вариант ответа')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    def __str__(self):
        return self.name
