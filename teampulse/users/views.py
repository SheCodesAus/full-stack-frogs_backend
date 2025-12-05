from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Count, Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Team, CustomUser
from event_logs.models import EventLog
from .serializers import TeamSerializer, CustomUserSerializer
from pulse_logs.utils import check_user_has_logged
from pulse_logs.serializers import PulseLogSerializer
from .permissions import IsOwner, IsStaff, IsSuperUser

class TeamDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]

    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializer(team) #we do not need many anymore, only unique instance is required
        return Response(serializer.data)
    
    def put(self, request, pk):
        print(f"updating: {pk}")
        team = self.get_object(pk) #giving the instance to the "serializers"-instance
        serializer = TeamSerializer(
            instance=team,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='team_updated',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   

class TeamList(APIView):

    def get(self, request):
        # Annotate the queryset with the count of related CustomUser objects where is_active is True
        teams = Team.objects.annotate(
            user_count=Count('customuser', filter=Q(customuser__is_active=True))
        )
        serializer = TeamSerializer(teams, many=True)
        
        # Inject the annotated count into the serialized data
        data = serializer.data
        for team, item in zip(teams, data):
            item['user_count'] = team.user_count
                
        # Check permissions using instances of the permission classes
        is_privileged = request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

        if not is_privileged:
            allowed_fields = {'id', 'team_name'}
            filtered_data = [
                {key: value for key, value in item.items() if key in allowed_fields}
                for item in data
            ]
            return Response(filtered_data)

        return Response(data)

    def post(self, request):
        # Check permissions: Allow only if SuperUser or Staff
        is_privileged = request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

        if not is_privileged:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='team_created',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff | IsOwner]

    def get_object(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user) #we do not need many anymore, only unique instance is required

        try:
            limit = int(request.query_params.get('limit', 26))
        except (ValueError, TypeError):
            limit = 26

        pulse_logs = user.logged_pulses.order_by('-year_week')[:limit]
        pulse_logs_serializer = PulseLogSerializer(pulse_logs, many=True)

        response_data = serializer.data
        response_data['logged_pulses'] = pulse_logs_serializer.data

        return Response(response_data)

    def put(self, request, pk):
        print(f"updating: {pk}")
        user = self.get_object(pk) #giving the instance to the "serializers"-instance
        serializer = CustomUserSerializer(
            instance=user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()

            user_data = {
                'id': serializer.data.get('id'),
                'username': serializer.data.get('username'),
                'is_staff': serializer.data.get('is_staff'),
                'is_active': serializer.data.get('is_active')
            }
            EventLog.objects.create(
                event_name='user_updated',
                version=0,
                metadata=user_data
            )

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomUserList(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            # Allow anyone to create a user (registration)
            permission_classes = [permissions.AllowAny]
        else:
            # Only allow authenticated Superusers or Staff to list users
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]

    def get(self, request): #getting a list of users
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request): #ability to create new users
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user_data = {
                'id': serializer.data.get('id'),
                'username': serializer.data.get('username'),
                'is_staff': serializer.data.get('is_staff')
            }
            EventLog.objects.create(
                event_name='user_created',
                version=0,
                metadata=user_data
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        has_logged = check_user_has_logged(user)

        logon_data = {
            'id': user.id,
            'username': user.username,
            'has_logged': has_logged
        }
        EventLog.objects.create(
            event_name='user_logged_on',
            version=0,
            metadata=logon_data
        )

        return Response({
            'token': token.key,
            'user_id': user.id,
            'is_staff': user.is_staff,
            'first_name': user.first_name,
            'team': user.team.id if user.team else None,
            'has_logged': has_logged
        })

class CustomUserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)

        return Response({
            'id': serializer.data.get('id'),
            'username': serializer.data.get('username'),
            'is_staff': serializer.data.get('is_staff'),
            'first_name': serializer.data.get('first_name'),
            'last_name': serializer.data.get('last_name'),
            'team': serializer.data.get('team').id if serializer.data.get('team') else None
        })
