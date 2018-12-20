from overflow_clone.models import (
    User,
    OverflowUser,
    Question,
    Answer,
    Comment,
    Tag)
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
            'body',
            'author',
            'tags',
            'vote',
            'answer',
            'comment',
            'date',
            'answered',
            'vote')


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
        model = Answer
        fields = (
            'body',
            'vote',
            'author',
            'date')


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('title')
