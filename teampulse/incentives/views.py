from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from django.db.models import Sum
from .models import Reward
from event_logs.models import EventLog
from .serializers import RewardSerializer
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