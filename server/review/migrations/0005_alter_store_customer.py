# Generated by Django 3.2.7 on 2022-07-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_auto_20220714_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='customer',
            field=models.ManyToManyField(blank=True, related_name='store_customers', to='review.Customer'),
        ),
    ]