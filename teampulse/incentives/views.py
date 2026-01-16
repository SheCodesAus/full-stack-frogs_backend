from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Reward, UserPoint
from event_logs.models import EventLog
from .serializers import RewardSerializer, UserPointSerializer
from users.permissions import IsOwner, IsStaff, IsSuperUser

class RewardDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]

    def get_object(self, pk):
        try:
            return Reward.objects.get(pk=pk)
        except Reward.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        reward = self.get_object(pk)
        serializer = RewardSerializer(
            instance=reward,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='reward_updated',
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class RewardList(APIView):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            # Allow any authenticated user to get reward list
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only allow authenticated Superusers or Staff to create rewards
            permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaff]
        return [permission() for permission in permission_classes]

    def get(self, request):
        rewards = Reward.objects.all()
        serializer = RewardSerializer(rewards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RewardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            EventLog.objects.create(
                event_name='reward_created',
                version=0,
                metadata=serializer.data
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPointDetail(APIView):
    
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsSuperUser]
    
    def get_object(self, pk):
        try:
            return UserPoint.objects.get(pk=pk)
        except UserPoint.DoesNotExist:
            raise Http404
        
    def put(self, request, pk):
        user_point = self.get_object(pk)
        serializer = UserPointSerializer(
            instance=user_point,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            
            EventLog.objects.create(
                event_name='userpoint_updated',
                version=0,
                metadata=serializer.data
            )
     
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class UserPointList(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.is_superuser:
            # Superusers see everything
            user_points = UserPoint.objects.all()
        else:
            # Regular users only see their own record
            user_points = UserPoint.objects.filter(user=request.user)
            
        serializer = UserPointSerializer(user_points, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Try to get existing points for this user
        instance = UserPoint.objects.filter(user=request.user).first()
        
        # If instance exists, serializer will update it; otherwise, it creates a new one
        serializer = UserPointSerializer(instance=instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            # If updating, we might want to ADD points rather than overwrite
            # You can handle that logic here or in the serializer's update()
            serializer.save(user=request.user)
            
            event_name = 'userpoint_updated' if instance else 'userpoint_created'
            EventLog.objects.create(
                event_name=event_name,
                version=0,
                metadata=serializer.data
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED if not instance else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
