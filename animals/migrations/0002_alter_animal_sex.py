# Generated by Django 4.1 on 2022-08-08 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Macho", "Macho"),
                    ("Femea", "Femea"),
                    ("Não informado", "Não Informado"),
                ],
                default="Não informado",
                max_length=15,
            ),
        ),
    ]
