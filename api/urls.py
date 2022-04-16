from rest_framework.routers import DefaultRouter
from .views import QuestionnaireViewSet, QuestionViewSet, ChoiceViewSet
from django.urls import path, include

router = DefaultRouter()

router.register('questionnaire', QuestionnaireViewSet)
router.register(
    'questionnaire/(?P<id>\d+)/questions',
    QuestionViewSet,
    basename='questions'
)
router.register(
    'questionnaire/(?P<id>\d+)/questions/(?P<question_pk>\d+)/choices',
    ChoiceViewSet,
    basename='choices'
)

urlpatterns = [
    path('', include(router.urls)),
]
