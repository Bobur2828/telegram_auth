# Generated by Django 5.0.3 on 2024-03-10 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='auth_type',
            new_name='auth_country',
        ),
    ]