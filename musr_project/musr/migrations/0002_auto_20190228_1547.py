# Generated by Django 2.1.7 on 2019-02-28 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("musr", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Following",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "followee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followee",
                        to="musr.Profile",
                    ),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follower",
                        to="musr.Profile",
                    ),
                ),
            ],
            options={"verbose_name_plural": "following"},
        ),
        migrations.AlterUniqueTogether(
            name="following", unique_together={("follower", "followee")}
        ),
    ]