from django.db import models
from django.contrib.auth.models import User

class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    create = models.CharField(max_length=255)
    study = models.CharField(max_length=255)
    work = models.CharField(max_length=255)
    feel = models.CharField(max_length=255)
    move = models.CharField(max_length=255)
    be = models.CharField(max_length=255)
    connect = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} on {self.submitted_at.strftime('%Y-%m-%d')}"
