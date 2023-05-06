# Generated by Django 4.2 on 2023-05-06 12:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0002_alter_project_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="status",
            field=models.CharField(
                choices=[("O", "Open"), ("IP", "In Progress"), ("C", "Closed")],
                default="O",
                max_length=3,
            ),
        ),
    ]
