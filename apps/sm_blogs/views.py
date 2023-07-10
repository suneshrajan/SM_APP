from rest_framework.views import APIView
from apps.sm_blogs.models import CommentPost, LikePost, UserPost
from apps.sm_users.models import UserFollower
from utils.permissions import CustomPermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from apps.sm_blogs.serializers import UserPostSerializers

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from utils.swgr_doc_schmas import UserBlogSchema, UserCommentSchema, \
    CreateUserBlogSchema, FollowerBlogSchema, LikePostSchema, UnLikePostSchema


class UserBlog(APIView):

    permission_classes = [CustomPermission]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=UserBlogSchema.get_tag(),
        operation_id=UserBlogSchema.get_operation_id(),
        operation_summary=UserBlogSchema.get_operation_summary(),
        operation_description=UserBlogSchema.get_operation_description(),
        responses=UserBlogSchema.get_responses()
    )
    def get(self, request):
        try:
            user_post_obj = UserPost.objects.filter(user_id=request.user.id)
            data = UserPostSerializers(user_post_obj, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        tags=CreateUserBlogSchema.get_tag(),
        operation_id=CreateUserBlogSchema.get_operation_id(),
        operation_summary=CreateUserBlogSchema.get_operation_summary(),
        operation_description=CreateUserBlogSchema.get_operation_description(),
        manual_parameters = CreateUserBlogSchema.get_manual_parameters(),
        consumes= CreateUserBlogSchema.get_consumes(),
        responses = CreateUserBlogSchema.get_responses()
    )
    def post(self, request):
        try:
            if 'content' in request.data:
                data = {
                    'content': request.data['content'],
                    'user': request.user.id
                }
                serializer = UserPostSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("Post added successfuly.", status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Please give valied data", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowerBlog(APIView):

    permission_classes = [CustomPermission]

    @swagger_auto_schema(
        tags=FollowerBlogSchema.get_tag(),
        operation_id=FollowerBlogSchema.get_operation_id(),
        operation_summary=FollowerBlogSchema.get_operation_summary(),
        operation_description=FollowerBlogSchema.get_operation_description(),
        responses=FollowerBlogSchema.get_responses()

    )
    def get(self, request):
        try:
            follower_list = UserFollower.objects.filter(user=request.user).values_list('user__userfollower__followers', flat=True)
            user_obj = UserPost.objects.filter(user_id__in=follower_list).order_by('-updated_at')
            data = UserPostSerializers(user_obj, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LikeBlog(APIView):

    permission_classes = [CustomPermission]

    @swagger_auto_schema(
        tags=LikePostSchema.get_tag(),
        operation_id=LikePostSchema.get_operation_id(),
        operation_summary=LikePostSchema.get_operation_summary(),
        operation_description=LikePostSchema.get_operation_description(),
        responses=LikePostSchema.get_responses()
    )
    def get(slef, request, post_id):
        try:
            if UserPost.objects.filter(id=post_id).exists():
                if LikePost.objects.filter(post_id=post_id, user_id=request.user.id).exists():
                    return Response("Already liked", status=status.HTTP_200_OK)
                else:
                    LikePost.objects.create(user=request.user, post_id=post_id)
                    return Response("Post liked successfully.", status=status.HTTP_201_CREATED)
            else:
                return Response("Post not found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        tags=UnLikePostSchema.get_tag(),
        operation_id=UnLikePostSchema.get_operation_id(),
        operation_summary=UnLikePostSchema.get_operation_summary(),
        operation_description=UnLikePostSchema.get_operation_description(),
        responses=UnLikePostSchema.get_responses()
    )
    def delete(slef, request, post_id):
        try:
            if UserPost.objects.filter(id=post_id).exists():
                if LikePost.objects.filter(post_id=post_id, user_id=request.user.id).exists():
                    LikePost.objects.filter(post_id=post_id, user_id=request.user.id).delete()
                    return Response("Successfully unliked", status=status.HTTP_200_OK)
                else:
                    return Response("Post not found.", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("Post not found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CommentBlog(APIView):

    permission_classes = [CustomPermission]
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(
        tags=UserCommentSchema.get_tag(),
        operation_id=UserCommentSchema.get_operation_id(),
        operation_summary=UserCommentSchema.get_operation_summary(),
        operation_description=UserCommentSchema.get_operation_description(),
        manual_parameters=UserCommentSchema.get_manual_parameters(),
        responses=UserCommentSchema.get_responses()
    )
    def post(slef, request):
        try:
            data = request.data
            if UserPost.objects.filter(id=data['post_id']).exists():
                CommentPost.objects.create(user=request.user, post_id=data['post_id'], content=data['comment'])
                return Response("Comment added successfully.", status=status.HTTP_201_CREATED)
            else:
                return Response("Post not found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f'Somthing went wrong: {e}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)