# Generated by Django 4.2.6 on 2023-10-30 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testapp1", "0002_file_temp_file_path_delete_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="temp_file_path",
            name="existingPath",
            field=models.CharField(max_length=100),
        ),
    ]
