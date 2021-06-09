# Generated by Django 3.1 on 2021-06-06 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("property", "0006_merge_20210606_0558"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="reply",
        ),
        migrations.RemoveField(
            model_name="reply",
            name="user",
        ),
        migrations.AddField(
            model_name="reply",
            name="reply_madeby",
            field=models.ForeignKey(
                blank=True,
                help_text="Reply made by user",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reply_madeby",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="reply",
            name="reply_madeto",
            field=models.ForeignKey(
                blank=True,
                help_text="Reply done to specific user comment",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reply_madeto",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]