# Generated by Django 4.1 on 2022-08-12 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0001_initial"),
        ("animals", "0004_alter_animal_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="groups.group"
            ),
        ),
    ]
