from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from overflow_clone.models import OverflowUser
from overflow_clone.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def signup_view(request):

    html = "signup.html"

    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        if User.objects.filter(username=data['username']).exists():
            return HttpResponseRedirect(reverse('homepage'))
        else:
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            login(request, user)
            OverflowUser.objects.create(name=user.username, user=user, bio="")
            return HttpResponseRedirect(reverse('login'))

    return render(request, html, {'form': form})

    return render(request, html)


def login_view(request):

    html = "login.html"

    form = LoginForm(None or request.POST)

    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password']
            )

        if user is not None:
            login(request, user)
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/")

    return render(request, html, {'form': form})


def logout_view(request):

    logout(request)

    return HttpResponseRedirect(reverse('homepage'))


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
