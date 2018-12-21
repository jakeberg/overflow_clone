from overflow_clone.models import (
    User,
    OverflowUser,
    Question,
    Answer,
    Comment,
    Tag)
from overflow_clone.serializers import (
    OverflowUserSerializer,
    QuestionSerializer,
    AnswerSerializer,
    CommentSerializer,
    TagSerializer)
from core.serializers import UserSerializer
from rest_framework import viewsets


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


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all answers
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
