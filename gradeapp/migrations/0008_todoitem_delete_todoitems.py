# Generated by Django 4.2.5 on 2023-10-06 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gradeapp", "0007_alter_todoitems_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="ToDoItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateField(blank=True, null=True)),
                ("progress", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
            },
        ),
        migrations.DeleteModel(
            name="ToDoItems",
        ),
    ]