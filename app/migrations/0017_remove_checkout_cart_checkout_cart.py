# Generated by Django 5.1.4 on 2025-03-16 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_customuser_is_customer_delete_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='cart',
        ),
        migrations.AddField(
            model_name='checkout',
            name='cart',
            field=models.ManyToManyField(to='app.cart'),
        ),
    ]
