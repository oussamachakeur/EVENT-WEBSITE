# Generated by Django 5.1.4 on 2025-02-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0002_alter_event_manager_alter_venue_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="manager",
            field=models.CharField(max_length=100, verbose_name="manager"),
        ),
    ]
