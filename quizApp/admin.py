from django.contrib import admin
from .models import QuestionModel, Topic, Result
# Register your models here.

admin.site.register(QuestionModel)
admin.site.register(Topic)
admin.site.register(Result)
