from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Sum
from .models import PulseLog, Mood, Workload
from event_logs.models import EventLog
from .serializers import MoodSerializer, WorkloadSerializer, PulseLogSerializer, PulseLogDetailSerializer
from .utils import get_time_index, check_user_has_logged
from users.permissions import IsOwner, IsStaff, IsSuperUser


class MoodDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]

    def get_object(self, pk):
        try:
            return Mood.objects.get(pk=pk)
        except Mood.DoesNotExist:
            raise Http404
        
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

            EventLog.objects.create(
                event_name='mood_updated',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   

class MoodList(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Allow anyone to get mood list
            permission_classes = [permissions.AllowAny]
        else:
            # Only allow authenticated Superusers or Staff to create moods
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]


    def get(self, request):
        moods = Mood.objects.all()
        serializer = MoodSerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='mood_created',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WorkloadList(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Allow anyone to get workload list
            permission_classes = [permissions.AllowAny]
        else:
            # Only allow authenticated Superusers or Staff to create workloads
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]


    def get(self, request):
        workloads = Workload.objects.all()
        serializer = WorkloadSerializer(workloads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkloadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='workload_created',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PulseLogList(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            # Allow anyone logged in to create pulse logs
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only allow authenticated Superusers or Staff to get pulse logs
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]

    def get(self, request):
        year_week = request.query_params.get('year_week')
        weeks_total = request.query_params.get('weeks_total')

        if year_week:
            pulse_logs = PulseLog.objects.filter(year_week=year_week)
        elif weeks_total:
            try:
                limit = int(weeks_total)
            except (ValueError, TypeError):
                limit = 13 # default fallback if invalid integer
            
            # Get the top 'limit' distinct year_week values
            top_weeks = PulseLog.objects.values_list('year_week', flat=True)\
                                        .distinct()\
                                        .order_by('-year_week')[:limit]
            
            # Filter logs belonging to those weeks
            pulse_logs = PulseLog.objects.filter(year_week__in=top_weeks)\
                                         .order_by('-year_week', '-timestamp')
        else:
            pulse_logs = PulseLog.objects.all()

        serializer = PulseLogSerializer(pulse_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PulseLogSerializer(data=request.data)
        if serializer.is_valid():
                
            timestamp_local = serializer.validated_data.get('timestamp_local')
            
            # Check if user has already logged for this week
            if check_user_has_logged(request.user, timestamp_local):

                attempt_data = {
                    'user': request.user.id,
                    'team': serializer.data.get('team'),
                    'mood': serializer.data.get('mood'),
                    'workload': serializer.data.get('workload'),
                    'comment': serializer.data.get('comment')
                }
                EventLog.objects.create(
                    event_name='duplicate_pulse_log_attempted',
                    version=0,
                    metadata=attempt_data
                )

                return Response(
                    {"detail": "You have already logged a pulse for this week."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            time_indices = get_time_index(timestamp_local)

            serializer.save(user=request.user, **time_indices)

            pulse_data = {
                'user': serializer.data.get('user'),
                'team': serializer.data.get('team'),
                'year_week': serializer.data.get('year_week'),
                'mood': serializer.data.get('mood'),
                'workload': serializer.data.get('workload'),
                'comment': serializer.data.get('comment')
            }
            EventLog.objects.create(
                event_name='pulse_log_created',
                version=0,
                metadata=pulse_data
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PulseLogDetail(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'PUT':
            # Allow only authenticated superuser to update pulse logs
            permission_classes = [permissions.IsAuthenticated, IsSuperUser]
        else:
            # Allow only authenticated Superusers or Staff to get pulse logs
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]

    def get_object(self, pk):
        try:
            return PulseLog.objects.get(pk=pk)
        except PulseLog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pulse_log = self.get_object(pk)
        serializer = PulseLogSerializer(pulse_log)
        return Response(serializer.data)

    def put(self, request, pk):
        pulse_log = self.get_object(pk)
        serializer = PulseLogDetailSerializer(
            instance=pulse_log,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():

            if serializer.validated_data.get('timestamp_local'):
                # If timestamp_local is provided, update the time indices
                # If user has provided year/week_index/year_week, it will be ignored in favour of timestamp_local
                timestamp_local = serializer.validated_data.get('timestamp_local')
                time_indices = get_time_index(timestamp_local)
                serializer.save(**time_indices)
            else:
                serializer.save()

            pulse_data = {
                'id': serializer.data.get('id'),
                'user': serializer.data.get('user'),
                'team': serializer.data.get('team'),
                'year_week': serializer.data.get('year_week'),
                'mood': serializer.data.get('mood'),
                'workload': serializer.data.get('workload'),
                'comment': serializer.data.get('comment')
            }
            EventLog.objects.create(
                event_name='pulse_log_updated',
                version=0,
                metadata=pulse_data
            )

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )