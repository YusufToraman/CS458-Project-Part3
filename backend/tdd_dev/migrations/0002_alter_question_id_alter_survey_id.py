# Generated by Django 5.1.6 on 2025-05-10 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdd_dev', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='survey',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
