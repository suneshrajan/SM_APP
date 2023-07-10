from rest_framework import serializers
from django.contrib.auth.models import User

from apps.sm_blogs.models import UserPost


class UserPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = ['id', 'user', 'content', 'image', 'created_at', 'updated_at']