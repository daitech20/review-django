# Generated by Django 3.2.7 on 2022-07-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_alter_store_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='full_name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
