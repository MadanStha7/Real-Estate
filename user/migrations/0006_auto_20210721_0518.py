# Generated by Django 3.1 on 2021-07-21 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_remove_agentdetail_accept_terms_and_condition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="full_name",
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(max_length=15),
        ),
    ]