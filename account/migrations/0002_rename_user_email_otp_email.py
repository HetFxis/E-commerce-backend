# Generated by Django 5.1.4 on 2025-03-17 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='user_email',
            new_name='email',
        ),
    ]
