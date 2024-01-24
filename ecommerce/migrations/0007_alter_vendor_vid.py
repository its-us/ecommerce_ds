# Generated by Django 5.0.1 on 2024-01-23 16:55

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_category_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='ven', unique=True),
        ),
    ]
