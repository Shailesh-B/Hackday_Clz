# Generated by Django 4.0.6 on 2022-07-15 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import webapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_rename_head_department_hod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_at',
        ),
        migrations.AddField(
            model_name='event',
            name='added_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='department',
            name='hod',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department', related_query_name='has_department', to=settings.AUTH_USER_MODEL, validators=[webapp.validators.validate_teacher]),
        ),
    ]
