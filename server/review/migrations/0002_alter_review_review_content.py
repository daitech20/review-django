# Generated by Django 4.0.5 on 2022-07-05 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_content',
            field=models.TextField(),
        ),
    ]
