# Generated by Django 3.1 on 2021-05-30 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210530_0746'),
        ('property', '0007_auto_20210530_0741'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to='user.agentdetail')),
                ('property_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_info', to='property.propertyinfo')),
            ],
            options={
                'verbose_name_plural': 'Contact Agent',
                'ordering': ['-id'],
            },
        ),
    ]