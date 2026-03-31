import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConstructionProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=150)),
                (
                    "project_type",
                    models.CharField(
                        choices=[
                            ("residential", "Residential"),
                            ("industrial", "Industrial"),
                            ("infrastructure", "Infrastructure"),
                            ("rehabilitation", "Rehabilitation"),
                        ],
                        max_length=20,
                    ),
                ),
                ("client_name", models.CharField(max_length=120)),
                ("site_address", models.CharField(max_length=180)),
                ("city", models.CharField(max_length=80)),
                ("project_manager", models.CharField(max_length=120)),
                ("engineer_in_charge", models.CharField(max_length=120)),
                ("contract_reference", models.CharField(max_length=40, unique=True)),
                ("start_date", models.DateField()),
                ("expected_end_date", models.DateField(blank=True, null=True)),
                (
                    "budget",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("planning", "Planning"),
                            ("execution", "Execution"),
                            ("on_hold", "On hold"),
                            ("completed", "Completed"),
                        ],
                        default="planning",
                        max_length=20,
                    ),
                ),
                ("progress_percentage", models.PositiveSmallIntegerField(default=0)),
                ("notes", models.TextField(blank=True)),
            ],
            options={"ordering": ["code"]},
        ),
        migrations.CreateModel(
            name="ProjectMaterial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("structure", "Structure"),
                            ("finishes", "Finishes"),
                            ("electrical", "Electrical"),
                            ("plumbing", "Plumbing"),
                            ("safety", "Safety"),
                        ],
                        max_length=20,
                    ),
                ),
                ("material_name", models.CharField(max_length=120)),
                ("supplier", models.CharField(max_length=120)),
                ("delivery_note", models.CharField(max_length=50)),
                ("batch_reference", models.CharField(blank=True, max_length=50)),
                ("storage_zone", models.CharField(max_length=80)),
                ("received_by", models.CharField(max_length=120)),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("kg", "Kilograms"),
                            ("m3", "Cubic meters"),
                            ("units", "Units"),
                            ("pallets", "Pallets"),
                            ("meters", "Meters"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "planned_quantity",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "received_quantity",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "consumed_quantity",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0.00"),
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "unit_cost",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                ("received_on", models.DateField()),
                ("quality_checked", models.BooleanField(default=False)),
                ("remarks", models.TextField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="materials",
                        to="projects.constructionproject",
                    ),
                ),
            ],
            options={"ordering": ["project__code", "-received_on", "material_name"]},
        ),
        migrations.AddConstraint(
            model_name="projectmaterial",
            constraint=models.UniqueConstraint(
                fields=("project", "delivery_note"),
                name="unique_delivery_note_per_project",
            ),
        ),
    ]

