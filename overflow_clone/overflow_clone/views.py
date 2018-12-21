from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from overflow_clone.models import OverflowUser, Question, Answer, Comment, Tag
from overflow_clone.forms import (
    SignupForm,
    LoginForm,
    QuestionForm,
    AnswerForm,
    UserSettingsUpdateForm
    )
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
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def logout_view(request):

    logout(request)

    return HttpResponseRedirect(reverse('homepage'))


def homepage_view(request, sort=None):

    html = "homepage.html"

    if sort:
        if sort == 'new':
            questions = Question.objects.order_by('-date')
        elif sort == 'upvote':
            questions = Question.objects.order_by('-vote')
        elif sort == 'tag':
            questions = set(Question.objects.order_by('tags'))
        elif sort == 'unanswered':
            questions = Question.objects.order_by('answered')
    else:
        questions = Question.objects.all()

    reputation = 0
    if request.user.is_authenticated:
        user = OverflowUser.objects.get(id=request.user.id)
        reputation = user.reputation

    content = {
        'questions': questions,
        'upvote_access': " " if reputation >= 15 else "disabled",
        'current_user': request.user
    }
    return render(request, html, content)


def question_form_view(request):
    form = QuestionForm(None or request.POST)
    html = "post.html"

    if form.is_valid():
        body = form.cleaned_data['body']
        tags = form.cleaned_data['tags']

        question = Question.objects.create(
            body=body,
            author=request.user.overflowuser
        )
        question.tags.set(tags)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form, 'form_name': 'Question'})


def bio_form_view(request):
    html = 'user_settings.html'
    user = OverflowUser.objects.filter(user=request.user).first()
    if request.method == 'POST':
        # Take the info from the POST and shove it in the db
        form = UserSettingsUpdateForm(request.POST or None)

        if form.is_valid():
            data = form.cleaned_data
            user.bio = data['bio']
            user.save()

            return render(request, 'homepage.html')

    else:
        # everything else will be a GET request
        form = UserSettingsUpdateForm(None)
    return render(request, html, {'form': form})


def answer_form_view(request, question_id):
    form = AnswerForm(None or request.POST)
    html = "post.html"

    if form.is_valid():
        body = form.cleaned_data['body']
        answer = Answer.objects.create(
            body=body,
            author=request.user.overflowuser
        )
        Question.objects.get(id=question_id).answer.add(answer)
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form, 'form_name': 'Answer'})


def upvote(request, vote_type, id):
    if vote_type == 'question':
        question = Question.objects.get(id=id)
        question.vote = question.vote + 1
        question.save()
        user = OverflowUser.objects.get(id=question.author.id)
        user.reputation = user.reputation + 5
        user.save()
    if vote_type == 'answer':
        answer = Answer.objects.get(id=id)
        answer.vote = answer.vote + 1
        answer.save()
        user = OverflowUser.objects.get(id=answer.author.id)
        user.reputation = user.reputation + 10
        user.save()
    if vote_type == 'comment':
        comment = Comment.objects.get(id=id)
        comment.vote = comment.vote + 1
        comment.save()
    return HttpResponseRedirect(reverse('homepage'))


def downvote(request, vote_type, id):
    if vote_type == 'question':
        question = Question.objects.get(id=id)
        question.vote = question.vote - 1
        question.save()
        user = OverflowUser.objects.get(id=question.author.id)
        user.reputation = user.reputation - 5
        user.save()
    if vote_type == 'answer':
        answer = Answer.objects.get(id=id)
        answer.vote = answer.vote - 1
        answer.save()
        user = OverflowUser.objects.get(id=answer.author.id)
        user.reputation = user.reputation - 10
        user.save()
    if vote_type == 'comment':
        comment = Comment.objects.get(id=id)
        comment.vote = comment.vote - 1
        comment.save()
    return HttpResponseRedirect(reverse('homepage'))


def user_profile_view(request, author_pk):
    html = 'user_profile.html'
    questions = Question.objects.filter(author_id=author_pk)
    user = OverflowUser.objects.filter(user=author_pk).first()
    current_user = request.user
    return render(request, html, {'questions': questions.values(),
                                  'user': user,
                                  'current_user': current_user
                                  })


def single_question_view(request, question_id):
    html = 'single_question.html'
    question = Question.objects.all().filter(id=question_id)
    reputation = 0

    if request.user.is_authenticated:
        user = OverflowUser.objects.get(id=request.user.id)
        reputation = user.reputation

    content = {
        'question': question,
        'upvote_access': " " if reputation >= 15 else "disabled",
        'current_user': request.user
    }
    print(content['question'])

    return render(request, html, {'question': content['question'][0]})
