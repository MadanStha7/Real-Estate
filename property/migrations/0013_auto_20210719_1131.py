# Generated by Django 3.1 on 2021-07-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0012_auto_20210718_1105"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="propertycategories",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="propertytypes",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]