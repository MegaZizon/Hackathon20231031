# Generated by Django 4.2.6 on 2023-10-31 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testapp1", "0010_alter_user_user_nickname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_nickname",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
