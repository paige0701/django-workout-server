from rest_framework import serializers
from django.contrib.auth.models import User
from workouts.models import Workout


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    workouts = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Workout.objects.all())

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'workouts', 'password')
