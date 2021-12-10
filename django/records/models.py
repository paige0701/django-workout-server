from django.db import models


# Create your models here.
class Record(models.Model):
    record_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    workout = models.ForeignKey('django.workouts.Workout', related_name='workouts', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('django.user.User', related_name='records', on_delete=models.CASCADE)
