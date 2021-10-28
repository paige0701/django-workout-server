from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from workouts.models import Workout
from workouts.serializers import WorkoutSerializer
from django.shortcuts import get_object_or_404


# Create your views here.
class WorkoutListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        workouts = Workout.objects.filter(show_yn='Y', user=request.user)
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


class WorkoutDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(Workout, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = WorkoutSerializer(obj, many=False)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, pk):
        workout = self.get_object(pk)
        workout.show_yn = 'N'
        workout.save()
        serializer = WorkoutSerializer(workout, many=False)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, pk):
        workout = self.get_object(pk)
        data = JSONParser().parse(request)
        workout.title = data['title']
        workout.save()
        serializer = WorkoutSerializer(workout, many=False)
        return JsonResponse(serializer.data, safe=False)
