from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Sum
from .models import PulseLog, Mood, Workload
from event_logs.models import EventLog
from .serializers import MoodSerializer, WorkloadSerializer, PulseLogSerializer


# from .permissions import IsOwnerOrReadOnly, isStaffOrReadOnly

class MoodList(APIView):

    def get(self, request):
        moods = Mood.objects.all()
        serializer = MoodSerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkloadList(APIView):

    def get(self, request):
        workloads = Workload.objects.all()
        serializer = WorkloadSerializer(workloads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkloadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PulseLogList(APIView):

    def get(self, request):
        pulse_logs = PulseLog.objects.all()
        serializer = PulseLogSerializer(pulse_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PulseLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PulseLogDetail(APIView):
    def get_object(self, pk):
        try:
            return PulseLog.objects.get(pk=pk)
        except PulseLog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pulse_log = self.get_object(pk)
        serializer = PulseLogSerializer(pulse_log)
        return Response(serializer.data)