# Generated by Django 4.0.6 on 2022-07-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_alter_discussion_options_alter_customuser_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
