# Generated by Django 4.2.5 on 2023-10-31 16:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testapp1", "0013_post_delete_liveroom_alter_user_user_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user_id",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="post",
            name="user_nickname",
            field=models.CharField(max_length=20),
        ),
    ]
