from django.db import models


class Workout(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show_yn = models.CharField(max_length=1, default='Y')
    user = models.ForeignKey('user.User', related_name='workouts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


