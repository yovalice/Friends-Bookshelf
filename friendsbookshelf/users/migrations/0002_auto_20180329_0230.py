# Generated by Django 2.0.3 on 2018-03-29 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendlist',
            old_name='accepted',
            new_name='accept',
        ),
        migrations.AddField(
            model_name='friendlist',
            name='decline',
            field=models.BooleanField(default=False),
        ),
    ]