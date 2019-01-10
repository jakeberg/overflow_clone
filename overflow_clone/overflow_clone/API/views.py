from overflow_clone.models import (
    User,
    OverflowUser,
    Question,
    Comment,
    Tag,
    Notification)
from overflow_clone.serializers import (
    OverflowUserSerializer,
    QuestionSerializer,
    CommentSerializer,
    TagSerializer,
    NotificationSerializer
    )
from core.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from overflow_clone.utils import (
    get_overflow_user,
    get_overflowuser_notifications,
    serve_questions,
    upvote_django_object,
    downvote_django_object
    )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OverflowUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all overflow user
    """
    queryset = OverflowUser.objects.all()
    serializer_class = OverflowUserSerializer

    @action(detail=False, methods=['post'])
    def overflow_user(self, request, pk=None):
        name = request.data['author']
        overflow_user = get_overflow_user(name)
        return Response({
            "name": overflow_user.name,
            "bio": overflow_user.bio,
            "reputation": overflow_user.reputation,
            "interests": overflow_user.interests.all().values(),
            "favorites": [i["id"] for i in
                          overflow_user.favorites.all().values()],
            "favorite_obj": overflow_user.favorites.all().values(),
            })


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['post'])
    def new(self, request, pk=None):
        data = request.data
        author = get_overflow_user(data['author'])
        tags = Tag.objects.filter(title__in=data['tags'])
        question = Question.objects.create(
            title=data['title'],
            body=data['body'],
            author=author
        )
        question.tags.set(tags)
        return Response(request.data)

    @action(detail=False)
    def date(self, request):
        date = Question.objects.all().order_by('-date')
        return Response(serve_questions(date))

    @action(detail=False)
    def tag(self, request):
        tag = Question.objects.all().order_by('tags')
        return Response(serve_questions(tag))

    @action(detail=False)
    def unanswered(self, request):
        unanswered = Question.objects.filter(answered=False)
        return Response(serve_questions(unanswered))

    @action(detail=False)
    def voted(self, request):
        voted = Question.objects.all().order_by('-vote')
        return Response(serve_questions(voted))

    @action(detail=False)
    def serve(self, request, pk=None):
        questions = Question.objects.all()
        served_questions = serve_questions(questions)
        return Response(served_questions)

    @action(detail=False, methods=['post'])
    def singleQuestion(self, request, pk=None):
        data = request.data
        question = Question.objects.filter(id=data['questionId'])
        return Response(serve_questions(question))

    @action(detail=False, methods=['post'])
    def upvote(self, request, pk=None):
        return upvote_django_object(request, Question)

    @action(detail=False, methods=['post'])
    def downvote(self, request, pk=None):
        return downvote_django_object(request, Question)

    @action(detail=False, methods=['post'])
    def favorite(self, request, pk=None):
        data = request.data
        overflow_user = get_overflow_user(data['author'])
        question = Question.objects.get(
            id=data['id']
            )
        favorites = overflow_user.favorites.all()
        if question not in favorites:
            overflow_user.favorites.add(question)
            return Response({"favorite": True})
        else:
            overflow_user.favorites.remove(question)
            return Response({"favorite": False})


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=['post'])
    def new(self, request, pk=None):
        data = request.data
        question = Question.objects.filter(
            body=data['question']['body']).first()
        new_comment_author = get_overflow_user(data['author'])
        new_comment = Comment.objects.create(
            body=data['comment'],
            author=new_comment_author
        )
        question.comment.add(new_comment)
        new_notification = Notification.objects.create(
            answer_user=new_comment_author,
            answer=new_comment,
            question=question
        )
        question.author.notifications.add(new_notification)
        return Response({
            'id': new_comment.id,
            'body': new_comment.body,
            'author': new_comment_author.name,
            'date': new_comment.date,
            'upvote': new_comment.upvote.all().values(),
            'downvote': new_comment.downvote.all().values(),
        })

    @action(detail=False, methods=['post'])
    def upvote(self, request, pk=None):
        return upvote_django_object(request, Comment)

    @action(detail=False, methods=['post'])
    def downvote(self, request, pk=None):
        return downvote_django_object(request, Comment)

    @action(detail=False, methods=['post'])
    def answer(self, request, pk=None):
        data = request.data
        question = Question.objects.filter(
            body=data['question']['body']).first()
        question_author = OverflowUser.objects.get(name=question.author.name)
        comment = Comment.objects.filter(body=data['comment']['body']).first()
        comment_author = OverflowUser.objects.get(name=comment.author.name)
        if question.answer.all().first() is None:
            question.answer.add(comment)
            comment_author.reputation += 15
            question_author.reputation += 2
            question.answered = True
            comment_author.save()
            question_author.save()
            question.save()
            return Response({'body': comment.body})
        elif comment in question.answer.all():
            question.answer.remove(comment)
            comment_author.reputation -= 15
            question_author.reputation -= 2
            question.answered = False
            comment_author.save()
            question_author.save()
            question.save()
            return Response({})


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all notifications
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['post'])
    def serve(self, request, pk=None):
        data = request.data
        notifications = get_overflowuser_notifications(data['author'])
        served_notifications = []
        for notification in notifications:
            served_notifications.append({
                'id': notification.id,
                'answer_user': notification.answer_user.name,
                'question': notification.question.title,
                'question_id': notification.question.id,
                'date': notification.date,
            })
        return Response(served_notifications)
