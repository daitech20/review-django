# Generated by Django 4.0.5 on 2022-07-06 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0005_store_remove_review_store_name_delete_configure_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='store_customers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_users', to=settings.AUTH_USER_MODEL),
        ),
    ]