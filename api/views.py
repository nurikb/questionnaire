from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from .models import Questionnaire, Choice, Question
from .serializers import QuestionnaireSerializer, QuestionSerializer, ChoiceSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

    def get_permissions(self):
        if self.action in [ 'list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create', 'destroy', 'update']:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, id=self.kwargs['id'])
        return questionnaire.questions.all()

    def perform_create(self, serializer):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['id'])
        serializer.save(questionnaire=questionnaire)

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [AllowAny, ]
        elif self.action in ['create', 'destroy', 'update']:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


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

