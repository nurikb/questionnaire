from rest_framework import serializers
from django.db.models import Q
from .models import Questionnaire, Question, Choice, Answer


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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Answer


class QuestionListSerializer(serializers.ModelSerializer):
    """Вопросы с ответами пользователя"""

    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = ['text', 'answers']
        model = Question

    def get_answers(self, question):
        author_id = self.context.get('request').user.id
        answers = Answer.objects.filter(
            Q(question=question) & Q(author__id=author_id))
        serializer = AnswerSerializer(instance=answers, many=True)
        return serializer.data


class UserQuestionnaireSerializer(serializers.ModelSerializer):
    """Опросы с вопросами и ответами пользователя"""

    questions = QuestionListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Questionnaire


class AdminQuestionListSerializer(serializers.ModelSerializer):
    """Вопросы с ответами всех пользователей"""

    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = ['text', 'answers']
        model = Question

    def get_answers(self, question):
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(instance=answers, many=True)
        return serializer.data


class AdminQuestionnaireSerializer(serializers.ModelSerializer):
    """Опросы с вопросами и ответами всех пользователей"""

    questions = AdminQuestionListSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Questionnaire


class AnswerOneTextSerializer(serializers.ModelSerializer):
    """Ответ своим текстом"""

    class Meta:
        fields = ['self_text']
        model = Answer


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        question_id = request.parser_context['kwargs'][
            'question_pk']

        queryset = super(UserFilteredPrimaryKeyRelatedField,
                         self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)


class AnswerOneChoiceSerializer(serializers.ModelSerializer):
    """Ответ с выбором одного варианта"""

    one_choice = UserFilteredPrimaryKeyRelatedField(
        many=False,
        queryset=Choice.objects.all()
    )

    class Meta:
        fields = ['one_choice']
        model = Answer


class AnswerMultipleChoiceSerializer(serializers.ModelSerializer):
    """Ответ с выбором нескольких вариантов"""

    many_choice = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=Choice.objects.all()
    )

    class Meta:
        fields = ['many_choice']
        model = Answer
