# Generated by Django 3.1 on 2021-06-24 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("property", "0009_auto_20210606_0904"),
    ]

    operations = [
        migrations.CreateModel(
            name="PropertyTypes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_propertytypes_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "PropertyTypes",
                "ordering": ["-created_on"],
            },
        ),
        migrations.CreateModel(
            name="PropertyCatgories",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Created at"
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="Last modified at"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="property_propertycatgories_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "PropertyCatgories",
                "ordering": ["-created_on"],
            },
        ),
        migrations.AddField(
            model_name="propertyinfo",
            name="property_categories",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="property_info",
                to="property.propertycatgories",
            ),
        ),
        migrations.AddField(
            model_name="propertyinfo",
            name="property_types",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="property_info",
                to="property.propertytypes",
            ),
        ),
    ]
