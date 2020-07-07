from django.db import models
from django.contrib.auth.models import User

# Create your models here.

Color_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    color = models.CharField(max_length=6, choices=Color_CHOICES, default='green')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


