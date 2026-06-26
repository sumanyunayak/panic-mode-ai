from django.db import models

class PanicSession(models.Model):
    situation = models.TextField()
    mood = models.CharField(max_length=50)
    diagnosis = models.CharField(max_length=200)
    severity = models.CharField(max_length=20)
    success_probability = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    conversation_history = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

class Task(models.Model):
    session = models.ForeignKey(PanicSession, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    start_time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    is_current = models.BooleanField(default=False)
    order = models.IntegerField(default=0)