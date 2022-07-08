# Generated by Django 4.0.5 on 2022-07-07 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_alter_store_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='customer_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]