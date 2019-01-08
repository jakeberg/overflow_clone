from overflow_clone.models import (
    OverflowUser,
    Question,
    Answer,
    Comment,
    Tag,
    Notification
    )
from rest_framework import serializers


class OverflowUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OverflowUser
        fields = (
            'name',
            'bio',
            'reputation',
            'interests',
            'favorites',
            'user')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Question
        fields = (
            'title',
            'body',
            'author',
            'tags',
            'answer',
            'comment',
            'date',
            'answered',
            'upvote',
            'downvote')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Answer
        fields = (
            'body',
            'author',
            'vote',
            'comment',
            'date')


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'body',
            'upvote',
            'downvote',
            'author',
            'date')


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('title',)


class NotificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Notification
        fields = (
            'answer_user',
            'answer',
            'question',
            'date'
        )
