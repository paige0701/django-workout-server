from rest_framework import serializers

from django.records.models import Record
from django.workouts.serializers import WorkoutSerializer


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    workout = WorkoutSerializer(many=False)

    class Meta:
        model = Record
        fields = ('id', 'user', 'workout', 'record_date',)
