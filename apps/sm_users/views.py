from rest_framework.permissions import IsAuthenticated
from apps.sm_users.models import UserFollower
from utils.permissions import CustomPermission
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserPrivateProfileSerializer, UserProfileSerializer
from utils.swgr_doc_schmas import *
from drf_yasg.utils import swagger_auto_schema


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=UserProfileSchema.get_tag(),
        operation_id=UserProfileSchema.get_operation_id(),
        operation_summary=UserProfileSchema.get_operation_summary(),
        operation_description = UserProfileSchema.get_operation_description(),
        responses = UserProfileSchema.get_responses()
    )
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_data = UserPrivateProfileSerializer(instance=user).data
            return Response({'data': user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UserListView(APIView):

    permission_classes = [CustomPermission]

    @swagger_auto_schema(
        tags=UserListSchema.get_tag(),
        operation_summary=UserListSchema.get_operation_summary(),
        operation_description = UserListSchema.get_operation_description(),
        responses = UserListSchema.get_responses()
    )
    def get(self, request):
        try:
            user = User.objects.all()
            user_data = UserPrivateProfileSerializer(instance=user, many=True).data
            return Response({'data': user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserSearchView(APIView):

    permission_classes = [CustomPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    @swagger_auto_schema(
        tags=UserListSchema.get_tag(),
        operation_id=UserListSchema.get_operation_id(),
        operation_summary=UserListSchema.get_operation_summary(),
        operation_description=UserListSchema.get_operation_description(),
        manual_parameters = UserListSchema.get_manual_parameters(),
        responses = UserListSchema.get_responses()
    )
    def get(self, request):
        try:
            search_term = request.GET.get('search', '')
            queryset = User.objects.filter(username__icontains=search_term) | User.objects.filter(first_name__icontains=search_term) | User.objects.filter(last_name__icontains=search_term)
            user_data = UserProfileSerializer(instance=queryset, many=True).data
            return Response({'data': user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserFollowerView(APIView):

    permission_classes = [CustomPermission]

    @swagger_auto_schema(
        tags=FollowerSchema.get_tag(),
        operation_id=FollowerSchema.get_operation_id(),
        operation_summary=FollowerSchema.get_operation_summary(),
        operation_description=FollowerSchema.get_operation_description(),
        responses = FollowerSchema.get_responses()
    )
    def post(self, request, user_id):
        try:
            user = request.user
            # Check if follower is exist
            if not User.objects.filter(id=user_id).exists():
                return Response("Follower does not exists or deactivated.", status=status.HTTP_404_NOT_FOUND)
            
            follower = User.objects.get(id=user_id)

            # Check if user already has fllowers
            if not UserFollower.objects.filter(user=user).exists():
                user_profile_obj = UserFollower.objects.create(user=user)
                user_profile_obj.followers.add(follower)

            elif UserFollower.objects.filter(user=user, followers=follower).exists():
                return Response("Already Following.", status=status.HTTP_200_OK)
            
            else:
                user_profile = UserFollower.objects.get(user=user)
                user_profile.followers.add(follower)

            return Response(f"Successfully followed user with ID {user_id}.", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        tags=UnFollowerSchema.get_tag(),
        operation_id=UnFollowerSchema.get_operation_id(),
        operation_summary=UnFollowerSchema.get_operation_summary(),
        operation_description=UnFollowerSchema.get_operation_description(),
        responses = UnFollowerSchema.get_responses()
    )
    def delete(self, request, user_id):
        try:
            user = request.user
            # Check if follower is exist
            if not User.objects.filter(id=user_id).exists():
                return Response("Follower does not exists or deactivated.", status=status.HTTP_404_NOT_FOUND)
            
            follower = User.objects.get(id=user_id)

            # Check if user already has fllowers
            if not UserFollower.objects.filter(user=user).exists():
                return Response("User don't have any follower please refresh the page.", status=status.HTTP_404_NOT_FOUND)
            
            if not UserFollower.objects.filter(user=user, followers=follower).exists():
                return Response("Already unfollowed.", status=status.HTTP_404_NOT_FOUND)
            
            user_profile = UserFollower.objects.get(user=user)
            user_profile.followers.remove(follower)
            
            return Response("Successfully unfollowed user with ID {user_id}.")
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)