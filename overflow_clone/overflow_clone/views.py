from django.shortcuts import render
from overflow_clone.models import OverflowUser
from django.contrib.auth.decorators import login_required


def homepage_view(request):

    html = "homepage.html"

    content = {
    }

    return render(request, html, content)


def question_form_view(request):

    html = "post.html"

    content = {
    }

    return render(request, html, content)