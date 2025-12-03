from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Sum
from .models import EventLog
from .serializers import EventLogSerializer
# from .permissions import IsOwnerOrReadOnly, isStaffOrReadOnly

class EventLogList(APIView):

    def get(self, request):
        # Order by timestamp descending (latest first)
        event_logs = EventLog.objects.all().order_by('-timestamp')
        serializer = EventLogSerializer(event_logs, many=True)

        return Response(serializer.data)