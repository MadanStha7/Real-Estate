# Generated by Django 3.1 on 2021-05-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffdetail',
            name='city',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='staffdetail',
            name='address',
            field=models.CharField(max_length=60, null=True),
        ),
    ]