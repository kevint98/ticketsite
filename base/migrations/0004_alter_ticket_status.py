# Generated by Django 4.2 on 2023-05-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_ticket_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="status",
            field=models.CharField(
                choices=[
                    ("Open", "Open"),
                    ("In Progress", "In Progress"),
                    ("Closed", "Closed"),
                ],
                default="Open",
                max_length=15,
            ),
        ),
    ]
