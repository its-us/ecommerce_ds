# Generated by Django 5.0.1 on 2024-02-12 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]