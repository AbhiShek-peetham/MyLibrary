# Generated by Django 5.1.2 on 2024-10-18 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_db', models.CharField(max_length=100)),
                ('email_db', models.CharField(max_length=100)),
                ('author_db', models.CharField(max_length=100)),
                ('price_db', models.IntegerField()),
            ],
        ),
    ]
