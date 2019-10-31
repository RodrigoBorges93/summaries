from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete = models.PROTECT)
    subject = models.CharField(max_length = 100, help_text = "Enter one or more subjects concerning your summary")
    summary = models.TextField(help_text = "Enter your summary")

    def __str__(self):
      return f'{self.user} summary {self.id}'
