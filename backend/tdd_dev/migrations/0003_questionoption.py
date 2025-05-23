# Generated by Django 5.1.6 on 2025-05-10 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdd_dev', '0002_alter_question_id_alter_survey_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='tdd_dev.question')),
            ],
        ),
    ]
