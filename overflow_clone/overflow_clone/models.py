from django.db import models
from django.contrib.auth.models import User


class OverflowUser(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    reputation = models.IntegerField(null=True)
    interests = models.ManyToManyField("Tag", symmetrical=False, blank=True)
    favorites = models.ManyToManyField("Question", symmetrical=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    body = models.TextField(max_length=150)
    author = models.ForeignKey(OverflowUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", symmetrical=False)
    comment = models.ManyToManyField("Comment", symmetrical=False)
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(OverflowUser, on_delete=models.CASCADE, null=True)
    vote = models.IntegerField()
    comment = models.ManyToManyField("Comment", symmetrical=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.name


class Comment(models.Model):
    body = models.CharField(max_length=20)
    vote = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(OverflowUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
