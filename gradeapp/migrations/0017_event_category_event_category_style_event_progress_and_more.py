# Generated by Django 4.2.5 on 2023-10-06 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gradeapp", "0016_todoitem_category_style"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="category",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="category_style",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="progress",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="progress_style",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
