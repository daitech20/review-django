# Generated by Django 3.2.7 on 2022-07-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_auto_20220715_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='customer',
            field=models.ManyToManyField(blank=True, null=True, related_name='store_customers', to='review.Customer'),
        ),
    ]
