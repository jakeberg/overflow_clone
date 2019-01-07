# Generated by Django 2.1.4 on 2019-01-07 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=150)),
                ('vote', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150)),
                ('vote', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OverflowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=50)),
                ('reputation', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='question', max_length=150)),
                ('body', models.TextField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('answered', models.BooleanField(default=False)),
                ('vote', models.IntegerField(default=0)),
                ('answer', models.ManyToManyField(blank=True, to='overflow_clone.Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overflow_clone.OverflowUser')),
                ('comment', models.ManyToManyField(blank=True, to='overflow_clone.Comment')),
                ('downvote', models.ManyToManyField(blank=True, related_name='downvote', to='overflow_clone.OverflowUser')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='overflow_clone.Tag'),
        ),
        migrations.AddField(
            model_name='question',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='upvote', to='overflow_clone.OverflowUser'),
        ),
        migrations.AddField(
            model_name='overflowuser',
            name='favorites',
            field=models.ManyToManyField(blank=True, to='overflow_clone.Question'),
        ),
        migrations.AddField(
            model_name='overflowuser',
            name='interests',
            field=models.ManyToManyField(blank=True, to='overflow_clone.Tag'),
        ),
        migrations.AddField(
            model_name='overflowuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='overflow_clone.OverflowUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='overflow_clone.OverflowUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='comment',
            field=models.ManyToManyField(to='overflow_clone.Comment'),
        ),
    ]
