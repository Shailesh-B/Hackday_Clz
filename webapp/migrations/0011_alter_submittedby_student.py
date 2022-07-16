# Generated by Django 4.0.6 on 2022-07-15 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import webapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_rename_user_submittedby_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedby',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, validators=[webapp.validators.validate_student]),
        ),
    ]
