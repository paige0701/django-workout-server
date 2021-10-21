from django.http import JsonResponse
from workouts.models import Workout
from workouts.serializers import WorkoutSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions

# Create your views here.
@csrf_exempt
def workout_list(request):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    if request.method == 'GET':
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WorkoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def perform_create(self, serializer):
    serializer.save(user=self.request.user)
