# Generated by Django 2.1.7 on 2019-03-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("musr", "0005_auto_20190314_1134")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="picture",
            field=models.ImageField(blank=True, upload_to="profile_images"),
        )
    ]
