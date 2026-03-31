from django.contrib import admin

from .models import ConstructionProject, ProjectMaterial


@admin.register(ConstructionProject)
class ConstructionProjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "project_type",
        "city",
        "status",
        "project_manager",
        "engineer_in_charge",
    )
    list_filter = ("project_type", "status", "city")
    search_fields = (
        "code",
        "name",
        "client_name",
        "project_manager",
        "engineer_in_charge",
        "contract_reference",
    )


@admin.register(ProjectMaterial)
class ProjectMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "material_name",
        "project",
        "category",
        "supplier",
        "delivery_note",
        "received_quantity",
        "consumed_quantity",
        "quality_checked",
    )
    list_filter = ("category", "unit", "quality_checked")
    search_fields = (
        "material_name",
        "supplier",
        "delivery_note",
        "project__code",
        "project__name",
    )

