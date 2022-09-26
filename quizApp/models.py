from django.db import models
from django.conf import settings

# Create your models here.

OPTION_CHOICES = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
)

TIME_CHOICES = (
    (5, "5 Mins"),(10, "10 Mins"),
    (15, "15 Mins"),(20, "20 Mins"),
    (25, "25 Mins"),(30, "30 Mins"),
    (35, "35 Mins"),(40, "40 Mins"),
    (45, "45 Mins"),(50, "50 Mins"),
    (55, "55 Mins"),(60, "60 Mins"),
)

class Topic(models.Model):
    name = models.CharField(max_length=80, verbose_name="Topic Name", unique=True)
    time = models.IntegerField(verbose_name="Total test time in minutes", choices=TIME_CHOICES)

    def __str__(self):
        return self.name

class QuestionModel(models.Model):

    question = models.CharField(max_length=500)
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200, choices = OPTION_CHOICES)
    topic = models.ForeignKey(Topic, related_name="questions", on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="result", on_delete=models.CASCADE)
    total_correct = models.PositiveIntegerField()
    total_question = models.PositiveIntegerField()
    date_time = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, related_name="results", on_delete=models.CASCADE)
    answers = models.JSONField()
    passed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return self.user.username
        
