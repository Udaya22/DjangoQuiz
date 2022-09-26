from django.urls import path, include
from .views import *

app_name="main"

urlpatterns = [
    path('',UserRegisterView.as_view(),name="signup"),
]