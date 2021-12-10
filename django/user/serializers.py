from rest_framework import serializers

from django.user.models import User
from django.workouts.models import Workout


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    workouts = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Workout.objects.all())

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'workouts', 'password')
