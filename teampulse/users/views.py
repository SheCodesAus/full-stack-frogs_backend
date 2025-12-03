from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Team, CustomUser
from event_logs.models import EventLog
from .serializers import TeamSerializer, CustomUserSerializer

# from .permissions import IsOwnerOrReadOnly, isStaffOrReadOnly

class TeamDetail(APIView):
    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        team = self.get_object(pk)
        serializer = TeamSerializer(team) #we donot need many anymore, only unique instance is required
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
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
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
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user) #we donot need many anymore, only unique instance is required
        return Response(serializer.data)
    
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

        logon_data = {
            'id': user.id,
            'username': user.username,
            'has_logged': None
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
            'team': user.team.id if user.team else None
        })