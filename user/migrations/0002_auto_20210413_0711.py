# Generated by Django 3.1 on 2021-04-13 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_verified',
        ),
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('modified_on', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified at')),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('count', models.PositiveBigIntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_userotp_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_otp', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Otp',
                'db_table': 'Otp',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_otp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile_otp', to='user.userotp'),
        ),
    ]