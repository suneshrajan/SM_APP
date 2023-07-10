from rest_framework import serializers

from django.db.models import Avg, Sum, Count, Max, Min
from django.contrib.auth.models import User
from apps.sm_users.models import ProfileImage, UserFollower
from apps.sm_blogs.models import UserPost

from apps.sm_blogs.serializers import UserPostSerializers

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ProfileImage
        fields = ['id', 'user', 'image']


class UserPrivateProfileSerializer(serializers.Serializer):

    def get_user_profile(self, instance):
        serializer = UserProfileSerializer(instance)
        return serializer.data

    def get_user_image(self, instance):
        if ProfileImage.objects.filter(user=instance.id).exists():
            profile_instance = ProfileImage.objects.get(user=instance.id)
            serializer = ProfileImageSerializer(profile_instance)
            return serializer.data
        else:
            return {'imge': ''}
    
    def get_user_following(self, instance):
        data = UserFollower.objects.filter(user_id=instance.id).aggregate(fllowing = Count('user__userfollower__followers'))
        return data
    
    def get_user_followers(self, instance):
        data = UserFollower.objects.filter(user__userfollower__followers=instance.id).aggregate(fllowers = Count('id'))
        return data

    def get_user_posts(self, instance):
        data = UserPost.objects.filter(user_id=instance.id).aggregate(posts = Count('id'))
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user_profile_data = self.get_user_profile(instance)
        user_image_data = self.get_user_image(instance)
        user_post_data = self.get_user_posts(instance)
        user_following_data = self.get_user_following(instance)
        user_follower_data = self.get_user_followers(instance)
        
        representation.update(user_profile_data)
        representation.update(user_image_data)
        representation.update(user_post_data)
        representation.update(user_following_data)
        representation.update(user_follower_data)

        return representation
