from time import process_time_ns
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from .models import QuestionModel, Result, Topic

from django.views import View

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User

# Create your views here.

class QuestionView(LoginRequiredMixin, ListView):
    model = QuestionModel
    template_name = 'quizApp/question_list.html'
    context_object_name = "questions"

    def get_queryset(self):
        return super().get_queryset().filter(topic_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.get(id=self.kwargs.get('pk'))
        context['time_mins'] = topic.time
        context['time_secs'] = 0
        return context

    def return_option(self, q, str_option):
        if str_option == "1":
            return q.option_1
        if str_option == "2":
            return q.option_2
        if str_option == "3":
            return q.option_3
        if str_option == "4":
            return q.option_4

    def post(self, request, **kwargs):
        questions = QuestionModel.objects.all().filter(topic_id=self.kwargs.get('pk'))
        total = QuestionModel.objects.filter(topic_id=self.kwargs.get('pk')).count()
        correct = 0
        json_result = {}

        for q in questions:
            json_ans = {}
            answered = "Not answered"

            if request.POST.get(q.question):
                answered = self.return_option(q, request.POST.get(q.question))

            if q.correct_option == request.POST.get(q.question):
                correct+=1

            correct_answer = self.return_option(q, q.correct_option)
            
            json_ans["Correct Answer"] = correct_answer
            json_ans["Selected Answered"] = answered
            json_result[q.question] = json_ans
            
        topic = Topic.objects.all().get(pk=self.kwargs.get('pk'))
        print(json_result)

        passed = False
        if correct/total >= 0.8:
            passed = True

        result = Result.objects.create(user=self.request.user,topic=topic, passed=passed,
        total_correct=correct, total_question=total, answers = json_result)
        return redirect("quizapp:score", pk=result.pk)

class CreateQuestion(CreateView):
    model = QuestionModel
    fields = ['topic', 'question', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']
    template_name = 'quizApp/question_form.html'
    
    def get_success_url(self):
        if "addnew" in self.request.POST:
            return reverse_lazy("quizapp:add_question")
        return reverse_lazy("quizapp:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            context = {"msg":"You are not authorized to access this page"}
        return context

class TestScore(View):

    def get(self, request, **kwargs):
        result = Result.objects.get(pk=kwargs.get("pk"))
        q_set = QuestionModel.objects.filter(topic_id=result.topic_id)
        if request.user!=result.user:
            return redirect("quizapp:all_results")

        # for q in q_set:
        #     print(type(result.option_selected[str(q.pk)]))

        return render(request, template_name="quizApp/results.html", context={"result":result})

class CreateTopic(CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("quizapp:admin_dash")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            context = {"msg":"You are not authorized to access this page"}
        return context

class TestDash(ListView):
    model = Topic
    template_name = "quizApp/test_dashboard.html"
    context_object_name = "topics"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("quizapp:admin_dash")
        return super().get(request, *args, **kwargs)
        
class ResultView(LoginRequiredMixin, ListView):
    model = Result

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user=self.request.user)
