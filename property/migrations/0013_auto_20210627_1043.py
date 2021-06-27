# Generated by Django 3.1 on 2021-06-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0012_auto_20210625_0707"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="propertyinfo",
            name="property_size",
        ),
        migrations.AddField(
            model_name="propertyinfo",
            name="property_size_type",
            field=models.CharField(
                choices=[("R", "Ropani"), ("A", "Aana"), ("S", "Square Feet")],
                max_length=1,
                null=True,
            ),
        ),
    ]
