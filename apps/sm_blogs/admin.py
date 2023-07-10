from django.contrib import admin
from apps.sm_blogs.models import CommentPost
from apps.sm_blogs.models import UserPost
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy


class CommentInline(admin.TabularInline):
    model = CommentPost
    extra = 0

# Implement search for our combain model[userpost, commentpost]
class PostAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'content', 'id' ]
    inlines = [CommentInline]


# Unregister Unwanted Models
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


# Register Needed Models
admin.site.register(UserPost, PostAdmin)