# Generated by Django 5.1.4 on 2025-02-07 09:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="venue",
            name="phone",
            field=models.CharField(
                blank=True, max_length=15, verbose_name="phone number"
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="web",
            field=models.URLField(blank=True, verbose_name="website url"),
        ),
    ]
