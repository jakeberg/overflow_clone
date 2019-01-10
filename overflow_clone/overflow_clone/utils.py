from core.serializers import UserSerializer
from overflow_clone.models import (
    User,
    OverflowUser
    )
from rest_framework.response import Response


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'author': UserSerializer(user, context={'request': request}).data
    }


def get_django_user(name):
    return User.objects.filter(username=name).first()


def get_overflow_user(name):
    user = get_django_user(name)
    return OverflowUser.objects.filter(user=user).first()


def get_overflowuser_notifications(name):
    user = get_overflow_user(name)
    return user.notifications.all()


def serve_questions(questions):
    served_questions = []
    for question in questions:
        author = OverflowUser.objects.filter(
            name=question.author.name).first().name
        tags = []
        for tag in question.tags.all():
            tags.append(tag.title)
        comments = []
        for comment in question.comment.all():
            comments.append({
                'id': comment.id,
                'body': comment.body,
                'date': comment.date,
                'author': comment.author.name,
                'upvote': comment.upvote.all().values(),
                'downvote': comment.downvote.all().values()
            })
        answer = question.answer.all().values().first() or {}
        served_questions.append({
            'id': question.id,
            'body': question.body,
            'author': author,
            'tags': tags,
            'upvote': question.upvote.all().values(),
            'downvote': question.downvote.all().values(),
            'comments': comments,
            'date': question.date,
            'answered': question.answered,
            'answer': answer,
            'title': question.title
        })
    return served_questions


def upvote_django_object(request, django_object):
    data = request.data
    upvoter = get_overflow_user(data['author'])
    object_owner = get_overflow_user(data['owner'])
    upvoted_object = django_object.objects.filter(
        id=data['id']
    ).first()
    upvote_rep_values = {
        'Question': {
            'upvote': 5,
            'downvote': 2
        },
        'Comment': {
            'upvote': 10,
            'downvote': 2
        }
    }
    if upvoter not in upvoted_object.upvote.all():
        upvoted_object.upvote.add(upvoter)
        object_owner.reputation += upvote_rep_values[django_object.__name__]['upvote']
    elif upvoter in upvoted_object.upvote.all():
        upvoted_object.upvote.remove(upvoter)
        object_owner.reputation -= upvote_rep_values[django_object.__name__]['upvote']
    if upvoter in upvoted_object.downvote.all():
        upvoted_object.downvote.remove(upvoter)
        object_owner.reputation += upvote_rep_values[django_object.__name__]['downvote']
    upvoted_object.save()
    object_owner.save()
    return Response({
        'downvote': upvoted_object.downvote.all().values(),
        'upvote': upvoted_object.upvote.all().values()
    })


def downvote_django_object(request, django_object):
    data = request.data
    downvoter = get_overflow_user(data['author'])
    object_owner = get_overflow_user(data['owner'])
    downvoted_object = django_object.objects.filter(
        id=data['id']
    ).first()
    downvote_rep_values = {
        'Question': {
            'upvote': 5,
            'downvote': 2
        },
        'Comment': {
            'upvote': 10,
            'downvote': 2
        }
    }
    if downvoter not in downvoted_object.downvote.all():
        downvoted_object.downvote.add(downvoter)
        object_owner.reputation -= downvote_rep_values[django_object.__name__]['downvote']
        downvoter.reputation -= 1
    elif downvoter in downvoted_object.downvote.all():
        downvoted_object.downvote.remove(downvoter)
        object_owner.reputation += downvote_rep_values[django_object.__name__]['downvote']
        downvoter.reputation += 1
    if downvoter in downvoted_object.upvote.all():
        downvoted_object.upvote.remove(downvoter)
        object_owner.reputation -= downvote_rep_values[django_object.__name__]['upvote']
    downvoted_object.save()
    object_owner.save()
    downvoter.save()
    return Response({
        'downvote': downvoted_object.downvote.all().values(),
        'upvote': downvoted_object.upvote.all().values()
    })