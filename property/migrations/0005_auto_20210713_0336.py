# Generated by Django 3.1 on 2021-07-13 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0004_auto_20210712_1104"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rentaldetails",
            name="basic_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rental_details",
                to="property.basicdetails",
            ),
        ),
    ]
