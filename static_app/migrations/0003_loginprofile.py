# Generated by Django 5.1.2 on 2024-10-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_app', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('password2', models.CharField(max_length=200)),
            ],
        ),
    ]
