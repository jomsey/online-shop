# Generated by Django 3.2.7 on 2022-04-17 11:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20220416_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]