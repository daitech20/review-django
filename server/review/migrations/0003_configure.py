# Generated by Django 4.0.5 on 2022-07-05 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0002_alter_review_review_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('domain', models.CharField(max_length=50)),
                ('store', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
