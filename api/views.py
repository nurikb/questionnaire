from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404

from .models import Questionnaire, Choice, Question, Answer
from .serializers import QuestionnaireSerializer, QuestionSerializer, ChoiceSerializer, AnswerOneTextSerializer, \
    AnswerOneChoiceSerializer, AnswerMultipleChoiceSerializer, AnswerSerializer, UserQuestionnaireSerializer, \
    AdminQuestionnaireSerializer
from django.db.models import Q


class PermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ['create', 'destroy', 'update']:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


class QuestionnaireViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class QuestionViewSet(PermissionMixin, viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, id=self.kwargs['id'])
        return questionnaire.questions.all()

    def perform_create(self, serializer):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['id'])
        serializer.save(questionnaire=questionnaire)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            questionnaire__id=self.kwargs['id'],
        )
        serializer.save(question=question)

    def get_queryset(self):
        question = get_object_or_404(Question, id=self.kwargs['question_pk'])
        return question.choices.all()


class AnswerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            questionnaire__id=self.kwargs['id'],
        )
        if question.question_type == 'text_field':
            return AnswerOneTextSerializer
        elif question.question_type == 'radio':
            return AnswerOneChoiceSerializer
        else:
            return AnswerMultipleChoiceSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            questionnaire__id=self.kwargs['id'],
        )
        answer = Answer.objects.filter(author=self.request.user, question=question).exists()
        print(answer)
        # if not answer:
        serializer.save(author=self.request.user, question=question)


class UserIdQuestionnaireListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = Questionnaire.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.is_staff:
            queryset = Questionnaire.objects.exclude(~Q(questions__answers__author__id__isnull=False))
        else:
            queryset = Questionnaire.objects.exclude(~Q(questions__answers__author__id=user_id))
        print(queryset)
        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminQuestionnaireSerializer
        return UserQuestionnaireSerializer


