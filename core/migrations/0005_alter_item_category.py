# Generated by Django 4.1 on 2022-08-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_item_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("P", "Pants"),
                    ("S", "Shirt"),
                    ("D", "Dress"),
                    ("SU", "Suits"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
