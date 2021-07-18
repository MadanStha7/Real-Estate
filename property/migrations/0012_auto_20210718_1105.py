# Generated by Django 3.1 on 2021-07-18 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0011_amenities_lift"),
    ]

    operations = [
        migrations.AlterField(
            model_name="amenities",
            name="basic_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="amenities",
                to="property.basicdetails",
            ),
        ),
    ]
