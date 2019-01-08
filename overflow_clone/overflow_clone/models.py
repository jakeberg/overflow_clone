from django.db import models
from django.contrib.auth.models import User


class OverflowUser(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    reputation = models.IntegerField(default=0)
    interests = models.ManyToManyField(
        "Tag",
        symmetrical=False,
        blank=True
        )
    favorites = models.ManyToManyField(
        "Question",
        symmetrical=False,
        blank=True
        )
    notifications = models.ManyToManyField(
        "Notification",
        symmetrical=False,
        blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.TextField(max_length=150, default="question")
    body = models.TextField(max_length=150)
    author = models.ForeignKey(OverflowUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        "Tag",
        symmetrical=False,
        blank=True)
    answer = models.ManyToManyField(
        "Comment",
        symmetrical=False,
        blank=True,
        related_name='question_answer')
    comment = models.ManyToManyField(
        "Comment",
        symmetrical=False,
        blank=True)
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    upvote = models.ManyToManyField(
        OverflowUser,
        symmetrical=False,
        blank=True,
        related_name='question_upvote'
    )
    downvote = models.ManyToManyField(
        OverflowUser,
        symmetrical=False,
        blank=True,
        related_name='question_downvote'
    )

    def __str__(self):
        return self.title


class Answer(models.Model):
    body = models.TextField(max_length=150)
    author = models.ForeignKey(
        OverflowUser,
        on_delete=models.CASCADE,
        null=True)
    vote = models.IntegerField(default=0)
    comment = models.ManyToManyField("Comment", symmetrical=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Comment(models.Model):
    body = models.CharField(max_length=150)
    upvote = models.ManyToManyField(
        OverflowUser,
        symmetrical=False,
        blank=True,
        related_name='comment_upvote'
    )
    downvote = models.ManyToManyField(
        OverflowUser,
        symmetrical=False,
        blank=True,
        related_name='comment_downvote'
    )
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        OverflowUser,
        on_delete=models.CASCADE,
        null=True
        )

    def __str__(self):
        return self.body


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Notification(models.Model):
    answer_user = models.ForeignKey(
        OverflowUser,
        on_delete=models.CASCADE
        )
    answer = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer
