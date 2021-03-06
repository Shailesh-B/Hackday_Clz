# Generated by Django 4.0.6 on 2022-07-15 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import webapp.utils
import webapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_eventmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmittedBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'ordering': ('submitted_at',),
            },
        ),
        migrations.RenameField(
            model_name='club',
            old_name='member',
            new_name='members',
        ),
        migrations.AddField(
            model_name='assignment',
            name='submitted_by',
            field=models.ManyToManyField(related_name='assignment', related_query_name='has_assignment', through='webapp.SubmittedBy', to=settings.AUTH_USER_MODEL, validators=[webapp.validators.validate_student]),
        ),
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to=settings.AUTH_USER_MODEL, validators=[webapp.validators.validate_student]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default='hello', upload_to='images/events/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='topic',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to=webapp.utils.upload_directory_path),
        ),
        migrations.AddField(
            model_name='submittedby',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.assignment'),
        ),
        migrations.AddField(
            model_name='submittedby',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
