# Generated by Django 4.1.7 on 2023-10-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default=False, max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default=False, max_length=30),
        ),
    ]