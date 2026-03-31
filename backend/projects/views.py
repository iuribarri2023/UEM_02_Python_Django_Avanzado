from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ConstructionProject, ProjectMaterial
from .permissions import GroupModelPermissions, ProjectMaterialsSummaryPermission
from .serializers import ConstructionProjectSerializer, ProjectMaterialSerializer


class ProjectQuerysetMixin:
    queryset = ConstructionProject.objects.all()
    serializer_class = ConstructionProjectSerializer
    permission_classes = [GroupModelPermissions]
    lookup_field = "code"
    lookup_url_kwarg = "code"


class MaterialQuerysetMixin:
    queryset = ProjectMaterial.objects.select_related("project").all()
    serializer_class = ProjectMaterialSerializer
    permission_classes = [GroupModelPermissions]


class ProjectViewSet(ProjectQuerysetMixin, viewsets.ModelViewSet):
    pass


class ProjectListAPIView(ProjectQuerysetMixin, generics.ListAPIView):
    pass


class ProjectCreateAPIView(ProjectQuerysetMixin, generics.CreateAPIView):
    pass


class ProjectDetailAPIView(ProjectQuerysetMixin, generics.RetrieveAPIView):
    pass


class ProjectUpdateAPIView(ProjectQuerysetMixin, generics.UpdateAPIView):
    pass


class MaterialListAPIView(MaterialQuerysetMixin, generics.ListAPIView):
    pass


class MaterialCreateAPIView(MaterialQuerysetMixin, generics.CreateAPIView):
    pass


class MaterialDetailAPIView(MaterialQuerysetMixin, generics.RetrieveAPIView):
    pass


class MaterialUpdateAPIView(MaterialQuerysetMixin, generics.UpdateAPIView):
    pass


@api_view(["GET"])
@permission_classes([ProjectMaterialsSummaryPermission])
def project_materials_summary(request, code):
    project = get_object_or_404(ConstructionProject, code=code)
    materials = project.materials.all().order_by("category", "material_name")

    totals = materials.aggregate(
        planned_total=Sum("planned_quantity"),
        received_total=Sum("received_quantity"),
        consumed_total=Sum("consumed_quantity"),
    )
    planned_total = totals["planned_total"] or Decimal("0.00")
    received_total = totals["received_total"] or Decimal("0.00")
    consumed_total = totals["consumed_total"] or Decimal("0.00")

    return Response(
        {
            "project": ConstructionProjectSerializer(project).data,
            "materials": ProjectMaterialSerializer(materials, many=True).data,
            "summary": {
                "planned_total": planned_total,
                "received_total": received_total,
                "consumed_total": consumed_total,
                "available_total": received_total - consumed_total,
                "material_entries": materials.count(),
            },
        },
        status=status.HTTP_200_OK,
    )

