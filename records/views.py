from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from records.models import Record
from records.serializers import RecordSerializer
from workouts.models import Workout
from workouts.serializers import WorkoutSerializer


class RecordMonthlyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        year, month = pk.split('-')
        records = Record.objects.filter(user=request.user,
                                        record_date__year=year,
                                        record_date__month=month)
        record_serializers = RecordSerializer(records, many=True)
        return JsonResponse(record_serializers.data, safe=False)


class RecordListView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = JSONParser().parse(request)
        workout = Workout.objects.get(id=data['workout'])
        workout_serializer = WorkoutSerializer(workout)
        data['workout'] = workout_serializer.data
        serializer = RecordSerializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer, workout)
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def perform_create(self, serializer, workout):
        serializer.save(user=self.request.user, workout=workout)


class RecordDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(Record, pk=pk)

    def get(self, request, pk):
        records = Record.objects.filter(user=request.user, record_date=pk)
        record_serializers = RecordSerializer(records, many=True)
        return JsonResponse(record_serializers.data, safe=False)

    def delete(self, request, pk):
        record = self.get_object(pk)
        record.delete()
        serializer = RecordSerializer(record, many=False)
        return JsonResponse(serializer.data, safe=False)
