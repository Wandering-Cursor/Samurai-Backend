# Generated by Django 5.0 on 2023-12-25 17:37

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_alter_baseuser_options_alter_overseer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='accounts.teacher')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('for_faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='accounts.faculty')),
                ('tasks', models.ManyToManyField(related_name='projects', to='administration.task')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
    ]
