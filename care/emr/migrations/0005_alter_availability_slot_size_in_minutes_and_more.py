# Generated by Django 5.1.3 on 2025-01-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emr", "0004_merge_20250108_1244"),
    ]

    operations = [
        migrations.AlterField(
            model_name="availability",
            name="slot_size_in_minutes",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="availability",
            name="tokens_per_slot",
            field=models.IntegerField(null=True),
        ),
    ]
