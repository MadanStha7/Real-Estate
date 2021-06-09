# Generated by Django 3.1 on 2021-06-04 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0004_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="propertydiscussionboard",
            options={
                "ordering": ["-id"],
                "verbose_name_plural": "Property Discussion Board",
            },
        ),
        migrations.AddField(
            model_name="comment",
            name="reply",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="property.comment",
            ),
        ),
    ]