from rest_framework import serializers

from .models import ConstructionProject, ProjectMaterial


class ConstructionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionProject
        fields = [
            "id",
            "code",
            "name",
            "project_type",
            "client_name",
            "site_address",
            "city",
            "project_manager",
            "engineer_in_charge",
            "contract_reference",
            "start_date",
            "expected_end_date",
            "budget",
            "status",
            "progress_percentage",
            "notes",
        ]

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        start_date = attrs.get("start_date", getattr(instance, "start_date", None))
        expected_end_date = attrs.get(
            "expected_end_date",
            getattr(instance, "expected_end_date", None),
        )
        progress_percentage = attrs.get(
            "progress_percentage",
            getattr(instance, "progress_percentage", 0),
        )

        if start_date and expected_end_date and expected_end_date < start_date:
            raise serializers.ValidationError(
                {"expected_end_date": "Expected end date cannot be earlier than the start date."}
            )

        if progress_percentage < 0 or progress_percentage > 100:
            raise serializers.ValidationError(
                {"progress_percentage": "Progress percentage must be between 0 and 100."}
            )

        return attrs


class ProjectMaterialSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source="project.code", read_only=True)
    available_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMaterial
        fields = [
            "id",
            "project",
            "project_code",
            "category",
            "material_name",
            "supplier",
            "delivery_note",
            "batch_reference",
            "storage_zone",
            "received_by",
            "unit",
            "planned_quantity",
            "received_quantity",
            "consumed_quantity",
            "available_quantity",
            "unit_cost",
            "total_cost",
            "received_on",
            "quality_checked",
            "remarks",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]

    def get_total_cost(self, obj):
        return obj.received_quantity * obj.unit_cost

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        planned_quantity = attrs.get("planned_quantity", getattr(instance, "planned_quantity", None))
        received_quantity = attrs.get("received_quantity", getattr(instance, "received_quantity", None))
        consumed_quantity = attrs.get("consumed_quantity", getattr(instance, "consumed_quantity", None))

        if (
            planned_quantity is not None
            and received_quantity is not None
            and received_quantity > planned_quantity
        ):
            raise serializers.ValidationError(
                {"received_quantity": "Received quantity cannot exceed the planned quantity."}
            )

        if (
            received_quantity is not None
            and consumed_quantity is not None
            and consumed_quantity > received_quantity
        ):
            raise serializers.ValidationError(
                {"consumed_quantity": "Consumed quantity cannot exceed the received quantity."}
            )

        return attrs
