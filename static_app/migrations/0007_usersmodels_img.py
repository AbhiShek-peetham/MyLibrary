# Generated by Django 5.1.2 on 2024-11-01 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_app', '0006_usersmodels_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmodels',
            name='img',
            field=models.ImageField(default=123, upload_to='books'),
            preserve_default=False,
        ),
    ]
