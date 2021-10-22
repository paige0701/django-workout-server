from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from workouts.models import Workout
from workouts.serializers import WorkoutSerializer


# Create your views here.
class WorkoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = WorkoutSerializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
