from overflow_clone.models import (
    User,
    OverflowUser,
    Question,
    Answer,
    Comment,
    Tag,
    Notification)
from overflow_clone.serializers import (
    OverflowUserSerializer,
    QuestionSerializer,
    AnswerSerializer,
    CommentSerializer,
    TagSerializer,
    NotificationSerializer
    )
from core.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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
        data = request.data
        user = User.objects.filter(username=data['author']).first()
        overflow_user = OverflowUser.objects.filter(user=user).first()
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
        user = User.objects.filter(username=data['author']).first()
        author = OverflowUser.objects.filter(user=user).first()
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

        page = self.paginate_queryset(date)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(date, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def tag(self, request):
        tag = Question.objects.order_by('tags')

        page = self.paginate_queryset(tag)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tag, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def unanswered(self, request):
        unanswered = Question.objects.order_by('answered')

        page = self.paginate_queryset(unanswered)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(unanswered, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def voted(self, request):
        voted = Question.objects.order_by('-vote')

        page = self.paginate_queryset(voted)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(voted, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def serve(self, request, pk=None):
        questions = Question.objects.all()
        served_questions = []
        for question in questions.all():
            author = OverflowUser.objects.filter(
                name=question.author.name).first().name
            tags = []
            for tag in question.tags.all():
                tags.append(tag.title)
            comments = []
            for comment in question.comment.all():
                comments.append({
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
        return Response(served_questions)

    @action(detail=False, methods=['post'])
    def singleQuestion(self, request, pk=None):
        data = request.data
        question = Question.objects.get(id=data['questionId'])
        author = OverflowUser.objects.filter(
            name=question.author.name).first().name
        tags = []
        for tag in question.tags.all():
            tags.append(tag.title)
        comments = []
        for comment in question.comment.all():
            comments.append({
                'body': comment.body,
                'date': comment.date,
                'author': comment.author.name,
                'upvote': comment.upvote.all().values(),
                'downvote': comment.downvote.all().values()
            })
        answer = question.answer.all().values().first() or {}
        singleQuestion = {
            'id': question.id,
            'body': question.body,
            'author': author,
            'tags': tags,
            'upvote': question.upvote.all().values(),
            'downvote': question.downvote.all().values(),
            'comments': comments,
            'date': question.date,
            'answered': question.answered,
            'answer': answer
        }
        return Response(singleQuestion)

    @action(detail=False, methods=['post'])
    def upvote(self, request, pk=None):
        data = request.data
        upvoter_user = User.objects.get(username=data['user'])
        upvoter = OverflowUser.objects.get(user=upvoter_user)
        question = Question.objects.filter(
            body=data['question']['body']
            ).first()
        question_author = OverflowUser.objects.get(name=question.author.name)
        if upvoter not in question.upvote.all():
            question.upvote.add(upvoter)
            question_author.reputation += 5
        elif upvoter in question.upvote.all():
            question.upvote.remove(upvoter)
            question_author.reputation -= 5
        if upvoter in question.downvote.all():
            question.downvote.remove(upvoter)
            question_author.reputation += 2
        question.save()
        question_author.save()
        return Response({
            'downvote': question.downvote.all().values(),
            'upvote': question.upvote.all().values()
            })

    @action(detail=False, methods=['post'])
    def downvote(self, request, pk=None):
        data = request.data
        downvoter_user = User.objects.get(username=data['user'])
        downvoter = OverflowUser.objects.get(user=downvoter_user)
        question = Question.objects.filter(
            body=data['question']['body']
            ).first()
        question_author = OverflowUser.objects.get(name=question.author.name)
        if downvoter not in question.downvote.all():
            question.downvote.add(downvoter)
            question_author.reputation -= 2
        elif downvoter in question.downvote.all():
            question.downvote.remove(downvoter)
            question_author.reputation += 2
        if downvoter in question.upvote.all():
            question.upvote.remove(downvoter)
            question_author.reputation -= 5
        question.save()
        question_author.save()
        return Response({
            'downvote': question.downvote.all().values(),
            'upvote': question.upvote.all().values()
            })

    @action(detail=False, methods=['post'])
    def favorite(self, request, pk=None):
        data = request.data
        favorite_user = User.objects.get(username=data['user'])
        overflow_user = OverflowUser.objects.get(user=favorite_user)
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

    @action(detail=False, methods=['post'])
    def new(self, request, pk=None):
        data = request.data
        user = User.objects.filter(username=data['author']).first()
        question = Question.objects.filter(
            body=data['question']['body']).first()
        new_comment_author = OverflowUser.objects.filter(user=user).first()
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
            'body': new_comment.body,
            'author': new_comment_author.name,
            'date': new_comment.date,
            'upvote': new_comment.upvote.all().values(),
            'downvote': new_comment.downvote.all().values(),
        })

    @action(detail=False, methods=['post'])
    def upvote(self, request, pk=None):
        data = request.data
        upvoter_user = User.objects.get(username=data['user'])
        upvoter = OverflowUser.objects.get(user=upvoter_user)
        comment = Comment.objects.filter(
            body=data['comment']['body']
            ).first()
        comment_author = OverflowUser.objects.get(name=comment.author.name)
        if upvoter not in comment.upvote.all():
            comment.upvote.add(upvoter)
            comment_author.reputation += 10
        elif upvoter in comment.upvote.all():
            comment.upvote.remove(upvoter)
            comment_author.reputation -= 10
        if upvoter in comment.downvote.all():
            comment.downvote.remove(upvoter)
            comment_author.reputation += 2
        comment.save()
        comment_author.save()
        return Response({
            'downvote': comment.downvote.all().values(),
            'upvote': comment.upvote.all().values()
            })

    @action(detail=False, methods=['post'])
    def downvote(self, request, pk=None):
        data = request.data
        downvoter_user = User.objects.get(username=data['user'])
        downvoter = OverflowUser.objects.get(user=downvoter_user)
        comment = Comment.objects.filter(
            body=data['comment']['body']
            ).first()
        comment_author = OverflowUser.objects.get(name=comment.author.name)
        if downvoter not in comment.downvote.all():
            comment.downvote.add(downvoter)
            comment_author.reputation -= 2
            downvoter.reputation -= 1
        elif downvoter in comment.downvote.all():
            comment.downvote.remove(downvoter)
            comment_author.reputation += 2
            downvoter.reputation += 1
        if downvoter in comment.upvote.all():
            comment.upvote.remove(downvoter)
            comment_author.reputation -= 2
        comment.save()
        return Response({
            'downvote': comment.downvote.all().values(),
            'upvote': comment.upvote.all().values()
            })

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
            return Response({'body': comment.body})
        elif comment in question.answer.all():
            question.answer.remove(comment)
            comment_author.reputation -= 15
            question_author.reputation -= 2
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
        user = OverflowUser.objects.filter(name=data['user']).first()
        notifications = user.notifications.all()
        served_notifications = []
        for notification in notifications:
            served_notifications.append({
                'answer_user': notification.answer_user.name,
                'question': notification.question.title,
                'question_id': notification.question.id,
                'date': notification.date,
            })
        return Response(served_notifications)
