"""
URL configuration for sm_account app.
"""
from django.urls import path
import apps.sm_users.views as USER

urlpatterns = [
    path('personal/profile/', USER.UserProfileView.as_view(), name="user-personal-profile"),
    # path('user_list/', USER.UserListView.as_view(), name="user_list"),
    path('user/<int:user_id>/follow/', USER.UserFollowerView.as_view(), name='follow_and_unfollow'),
    path('search/user/', USER.UserSearchView.as_view(), name='search-user'),
]