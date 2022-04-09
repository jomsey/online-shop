# Generated by Django 3.2.7 on 2022-04-09 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20220409_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 'very poor'), (2, 'poor'), (3, 'good'), (4, 'very good'), (5, 'excellent')], null=True, verbose_name='product_rating'),
        ),
    ]
