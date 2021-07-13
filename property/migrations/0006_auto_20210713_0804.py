# Generated by Django 3.1 on 2021-07-13 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0005_auto_20210713_0336"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="localitydetails",
            options={
                "ordering": ["-created_on"],
                "verbose_name_plural": "LocalityDetails",
            },
        ),
        migrations.AlterModelOptions(
            name="rentaldetails",
            options={
                "ordering": ["-created_on"],
                "verbose_name_plural": "Rental Details",
            },
        ),
        migrations.AlterModelTable(
            name="localitydetails",
            table=None,
        ),
        migrations.AlterModelTable(
            name="rentpropertydetails",
            table=None,
        ),
    ]
