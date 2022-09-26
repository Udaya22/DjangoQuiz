from django.urls import path
from .views import QuestionView, CreateQuestion, ResultView, CreateTopic, TestDash, TestScore

from django.views.generic import TemplateView

app_name="quizapp"

urlpatterns = [
    path('start-test/<pk>',QuestionView.as_view(),name="start_test"),
    path('add-question',CreateQuestion.as_view(),name='add_question'),
    path('add-topic',CreateTopic.as_view(),name='add_topic'),
    path('test-score/<pk>',TestScore.as_view(),name='score'),
    path('results/all',ResultView.as_view(),name='all_results'),
    path('admin-dashboard', TemplateView.as_view(template_name="quizApp/admin_dashboard.html"), name="admin_dash"),
    path('', TestDash.as_view(), name="home"),
]