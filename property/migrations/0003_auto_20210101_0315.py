# Generated by Django 3.1 on 2021-01-01 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_fieldvisit_propertydiscussionboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='uid',
            field=models.UUIDField(auto_created=True, blank=True, null=True, unique=True),
        ),
    ]
