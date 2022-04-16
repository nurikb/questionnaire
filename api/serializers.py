from rest_framework import serializers
from .models import Questionnaire, Question, Choice


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Choice
