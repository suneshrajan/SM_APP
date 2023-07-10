"""
URL configuration for sm_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="SM API",
        default_version='v1',
        description="""
            Description
            -----------

            The developed APIs for the social media platform provide a comprehensive set of functionalities to allow users to 
            create accounts, log in and out, verify their email addresses, create posts with text and image attachments, follow and unfollow other users, 
            view a timeline of posts from followed users, like and comment on posts, view user profiles with relevant information, 
            search for other users by username or name, and provide an admin(**http://127.0.0.1:8000/admin/**) interface for managing users, posts, and comments.
            NOTE - Developers: Here we are not allowing creating admin automatically, so plese makse sure that have admin account.

            - The APIs are designed to be user-friendly, secure, and efficient. They handle various error scenarios and provide appropriate error responses to 
            ensure data integrity and smooth user experience. The implementation includes unit tests to verify the correctness and functionality of the APIs.

            - Furthermore, a background task using Celery is implemented to fetch and deactivate users with unverified email addresses daily at 7 pm, 
            ensuring the platform maintains active and verified user accounts. 
            NOTE: **celery -A sm_backend worker -B --loglevel=info** use this comend to schedule, run celery task.

            - To facilitate API usage and integration, comprehensive API documentation is provided using Swagger. The documentation includes detailed descriptions, 
            request and response examples, and clear instructions on how to interact with each API endpoint.

            - In conclusion, the developed APIs for the social media platform offer a robust and scalable solution for building a social media application, 
            enabling users to connect, share, and interact within the platform's ecosystem.
        """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.sm_accounts.urls')),
    path('api/users/', include('apps.sm_users.urls')),
    path('api/blogs/', include('apps.sm_blogs.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
