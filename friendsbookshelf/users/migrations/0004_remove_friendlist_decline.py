# Generated by Django 2.0.3 on 2018-04-16 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendlist',
            name='decline',
        ),
    ]