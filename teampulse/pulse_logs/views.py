from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Sum
from .models import PulseLog, Mood, Workload
from .serializers import MoodSerializer
from .serializers import WorkloadSerializer
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
    
    def put(self, request, pk):
        print(f"updating: {pk}")
        mood = self.get_object(pk) #giving the instance to the "serializers"-instance
        serializer = MoodSerializer(
            instance=mood,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   

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
    
    def put(self, request, pk):
        print(f"updating: {pk}")
        workload = self.get_object(pk) #giving the instance to the "serializers"-instance
        serializer = WorkloadSerializer(
            instance=workload,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   