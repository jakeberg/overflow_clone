"""overflow_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from overflow_clone.models import (
    OverflowUser,
    Question,
    Comment,
    Tag,
    Notification
)
from overflow_clone.API.views import (
    UserViewSet,
    OverflowUserViewSet,
    QuestionViewSet,
    CommentViewSet,
    TagViewSet,
    NotificationViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'overflow-users', OverflowUserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'notifications', NotificationViewSet)

admin.site.register(OverflowUser)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Notification)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework')),
    path('token-auth/', obtain_jwt_token),
    path('core/', include('core.urls')),
]
