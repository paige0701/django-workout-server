from rest_framework import serializers
from .models import Workout
from django.contrib.auth.models import User


class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Workout
        fields = ('id', 'title', 'created_at', 'updated_at', 'show_yn', 'user',)


class UserSerializer(serializers.ModelSerializer):
    workouts = serializers.PrimaryKeyRelatedField(many=True, queryset=Workout.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'workouts']
