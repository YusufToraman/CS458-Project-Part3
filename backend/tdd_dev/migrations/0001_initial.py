# Generated by Django 5.1.6 on 2025-05-10 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('question_type', models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('rating', 'Rating'), ('text', 'Open Text'), ('dropdown', 'Dropdown'), ('checkbox', 'Checkbox')], max_length=50)),
                ('condition_answer', models.CharField(blank=True, max_length=255, null=True)),
                ('condition_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conditional_questions', to='tdd_dev.question')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tdd_dev.survey')),
            ],
        ),
    ]
