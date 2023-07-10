"""
URL configuration for sm_blogs app.
"""
from django.urls import path
import apps.sm_blogs.views as BLOG

urlpatterns = [
    path('user/personal/post/', BLOG.UserBlog.as_view(), name="user-blog"),
    path('user/following/post/', BLOG.FollowerBlog.as_view(), name="follower-blog"),
    path('user/following/<int:post_id>/post/', BLOG.LikeBlog.as_view(), name="like-unlike-blog"),
    path('user/following/post/comment/', BLOG.CommentBlog.as_view(), name="comment-blog")
]