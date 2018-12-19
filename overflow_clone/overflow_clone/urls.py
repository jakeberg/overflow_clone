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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from overflow_clone.views import (
    homepage_view,
    signup_view,
    login_view,
    logout_view,
    question_form_view,
    answer_form_view,
    upvote,
    downvote
)
from overflow_clone.models import (
    OverflowUser,
    Question,
    Answer,
    Comment,
    Tag)

admin.site.register(OverflowUser)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Tag)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('home/', homepage_view, name='homepage'),
    path('home/<sort>', homepage_view),
    path('signup/', signup_view),
    path('login/', login_view, name='login'),
    path('logout/', logout_view),
    path('post/', question_form_view,),
    path('answer/<int:question_id>', answer_form_view,),
    path('upvote/<vote_type>/<int:id>', upvote),
    path('downvote/<vote_type>/<int:id>', downvote),
]
