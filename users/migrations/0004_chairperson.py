# Generated by Django 4.2.5 on 2023-09-25 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_student_has_submitted_feedback_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chairperson',
            fields=[
                ('full_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
