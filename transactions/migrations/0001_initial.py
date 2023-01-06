# Generated by Django 4.1.5 on 2023-01-06 17:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=15)),
                ("description", models.CharField(max_length=255)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("payment", "Pmt"), ("receipt", "Rct")], max_length=7
                    ),
                ),
                ("transaction_date", models.DateField()),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="accounts.account",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="categories.categories",
                    ),
                ),
            ],
        ),
    ]