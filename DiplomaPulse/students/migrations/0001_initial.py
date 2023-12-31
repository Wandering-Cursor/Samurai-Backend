# Generated by Django 5.0 on 2023-12-27 15:12

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_baseuser_options_alter_overseer_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='comments')),
                ('text', models.TextField(blank=True, default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('state', models.CharField(choices=[('new', 'New'), ('in_progress', 'In progress'), ('in_review', 'In review'), ('reopened', 'Reopened'), ('done', 'Done')], default='new', max_length=255)),
                ('due_date', models.DateField(blank=True, help_text='The date when this task should be completed', null=True)),
                ('comments', models.ManyToManyField(blank=True, related_name='comments', to='students.comment')),
                ('reviewer', models.ForeignKey(blank=True, help_text='The teacher who will review this task', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to='accounts.teacher')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('theme', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to='accounts.student')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to='accounts.teacher')),
                ('tasks', models.ManyToManyField(related_name='user_projects', to='students.usertask')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
