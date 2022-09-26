from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import UserRegisterForm
from django.urls import reverse_lazy
# Create your views here.

class UserRegisterView(CreateView):
    
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'useraccounts/signup.html'


    
