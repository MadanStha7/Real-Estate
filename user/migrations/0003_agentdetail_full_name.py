# Generated by Django 3.1 on 2021-06-04 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_notificationactivity_notificatons"),
    ]

    operations = [
        migrations.AddField(
            model_name="agentdetail",
            name="full_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]