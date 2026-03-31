from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class ConstructionProject(models.Model):
    class ProjectType(models.TextChoices):
        RESIDENTIAL = "residential", "Residential"
        INDUSTRIAL = "industrial", "Industrial"
        INFRASTRUCTURE = "infrastructure", "Infrastructure"
        REHABILITATION = "rehabilitation", "Rehabilitation"

    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        EXECUTION = "execution", "Execution"
        ON_HOLD = "on_hold", "On hold"
        COMPLETED = "completed", "Completed"

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    project_type = models.CharField(max_length=20, choices=ProjectType.choices)
    client_name = models.CharField(max_length=120)
    site_address = models.CharField(max_length=180)
    city = models.CharField(max_length=80)
    project_manager = models.CharField(max_length=120)
    engineer_in_charge = models.CharField(max_length=120)
    contract_reference = models.CharField(max_length=40, unique=True)
    start_date = models.DateField()
    expected_end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    progress_percentage = models.PositiveSmallIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class ProjectMaterial(models.Model):
    class Category(models.TextChoices):
        STRUCTURE = "structure", "Structure"
        FINISHES = "finishes", "Finishes"
        ELECTRICAL = "electrical", "Electrical"
        PLUMBING = "plumbing", "Plumbing"
        SAFETY = "safety", "Safety"

    class Unit(models.TextChoices):
        KG = "kg", "Kilograms"
        M3 = "m3", "Cubic meters"
        UNITS = "units", "Units"
        PALLETS = "pallets", "Pallets"
        METERS = "meters", "Meters"

    project = models.ForeignKey(
        ConstructionProject,
        on_delete=models.CASCADE,
        related_name="materials",
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    material_name = models.CharField(max_length=120)
    supplier = models.CharField(max_length=120)
    delivery_note = models.CharField(max_length=50)
    batch_reference = models.CharField(max_length=50, blank=True)
    storage_zone = models.CharField(max_length=80)
    received_by = models.CharField(max_length=120)
    unit = models.CharField(max_length=20, choices=Unit.choices)
    planned_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    received_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    consumed_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    received_on = models.DateField()
    quality_checked = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["project__code", "-received_on", "material_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "delivery_note"],
                name="unique_delivery_note_per_project",
            )
        ]

    def __str__(self):
        return f"{self.project.code} - {self.material_name} ({self.delivery_note})"

    @property
    def available_quantity(self):
        return self.received_quantity - self.consumed_quantity

