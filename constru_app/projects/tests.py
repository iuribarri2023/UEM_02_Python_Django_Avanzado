from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import ConstructionProject, ProjectMaterial
from .permissions import ENGINEERS_GROUP, WORKERS_GROUP


class ProjectsApiTests(APITestCase):
    def setUp(self):
        self.project = ConstructionProject.objects.create(
            code="OBR-001",
            name="Residential Tower Aravaca",
            project_type=ConstructionProject.ProjectType.RESIDENTIAL,
            client_name="Habitat Europa",
            site_address="Avenida de la Obra 14",
            city="Madrid",
            project_manager="Laura Torres",
            engineer_in_charge="Carlos Mendez",
            contract_reference="CTR-ARV-2026-01",
            start_date="2026-04-01",
            expected_end_date="2027-03-31",
            budget="2750000.00",
            status=ConstructionProject.Status.EXECUTION,
            progress_percentage=18,
            notes="Foundation and retaining walls in progress.",
        )
        self.material = ProjectMaterial.objects.create(
            project=self.project,
            category=ProjectMaterial.Category.STRUCTURE,
            material_name="HA-25 concrete",
            supplier="Hormigones Centro",
            delivery_note="ALB-0001",
            batch_reference="LOT-HA25-APR",
            storage_zone="North silo",
            received_by="Miguel Ruiz",
            unit=ProjectMaterial.Unit.M3,
            planned_quantity="180.00",
            received_quantity="110.00",
            consumed_quantity="75.00",
            unit_cost="92.50",
            received_on="2026-04-10",
            quality_checked=True,
            remarks="Delivery accepted after slump test.",
        )

        self.engineers_group, _ = Group.objects.get_or_create(name=ENGINEERS_GROUP)
        self.workers_group, _ = Group.objects.get_or_create(name=WORKERS_GROUP)
        self._assign_permissions()

        self.engineer = User.objects.create_user(username="engineer", password="engineer123")
        self.engineer.groups.add(self.engineers_group)
        self.engineer_token = Token.objects.create(user=self.engineer)

        self.worker = User.objects.create_user(username="worker", password="worker123")
        self.worker.groups.add(self.workers_group)
        self.worker_token = Token.objects.create(user=self.worker)

    def _assign_permissions(self):
        engineer_permissions = Permission.objects.filter(
            codename__in=[
                "add_constructionproject",
                "change_constructionproject",
                "delete_constructionproject",
                "view_constructionproject",
                "add_projectmaterial",
                "change_projectmaterial",
                "delete_projectmaterial",
                "view_projectmaterial",
            ]
        )
        worker_permissions = Permission.objects.filter(
            codename__in=[
                "view_constructionproject",
                "view_projectmaterial",
                "add_projectmaterial",
            ]
        )
        self.engineers_group.permissions.set(engineer_permissions)
        self.workers_group.permissions.set(worker_permissions)

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_engineer_can_create_project_from_viewset(self):
        self.authenticate(self.engineer_token)
        response = self.client.post(
            reverse("project-viewset-list"),
            data={
                "code": "OBR-002",
                "name": "Industrial Logistics Warehouse",
                "project_type": ConstructionProject.ProjectType.INDUSTRIAL,
                "client_name": "Norte Logistica",
                "site_address": "Parcela 9, Poligono Norte",
                "city": "Guadalajara",
                "project_manager": "Elena Diaz",
                "engineer_in_charge": "Ruben Perez",
                "contract_reference": "CTR-IND-2026-09",
                "start_date": "2026-05-01",
                "expected_end_date": "2027-02-15",
                "budget": "3200000.00",
                "status": ConstructionProject.Status.PLANNING,
                "progress_percentage": 0,
                "notes": "Pending site fencing and survey staking.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_worker_can_list_projects_but_cannot_create_them(self):
        self.authenticate(self.worker_token)
        list_response = self.client.get(reverse("project-list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        create_response = self.client.post(
            reverse("project-create"),
            data={
                "code": "OBR-003",
                "name": "Unauthorized Project",
                "project_type": ConstructionProject.ProjectType.REHABILITATION,
                "client_name": "Cliente",
                "site_address": "Calle Falsa 123",
                "city": "Toledo",
                "project_manager": "No Permitido",
                "engineer_in_charge": "No Permitido",
                "contract_reference": "CTR-NO-2026-77",
                "start_date": "2026-06-01",
                "expected_end_date": "2026-12-01",
                "budget": "1000.00",
                "status": ConstructionProject.Status.PLANNING,
                "progress_percentage": 0,
                "notes": "",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 403)

    def test_worker_can_add_material_but_cannot_update_it(self):
        self.authenticate(self.worker_token)
        create_response = self.client.post(
            reverse("material-create"),
            data={
                "project": self.project.id,
                "category": ProjectMaterial.Category.SAFETY,
                "material_name": "Protective helmets",
                "supplier": "Seguridad Obra SL",
                "delivery_note": "ALB-0015",
                "batch_reference": "SAF-APR-15",
                "storage_zone": "Container A",
                "received_by": "Jorge Cano",
                "unit": ProjectMaterial.Unit.UNITS,
                "planned_quantity": "60.00",
                "received_quantity": "40.00",
                "consumed_quantity": "0.00",
                "unit_cost": "18.00",
                "received_on": "2026-04-18",
                "quality_checked": True,
                "remarks": "Initial PPE batch.",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        update_response = self.client.patch(
            reverse("material-update", args=[create_response.data["id"]]),
            data={"consumed_quantity": "5.00"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 403)

    def test_engineer_can_update_materials(self):
        self.authenticate(self.engineer_token)
        response = self.client.patch(
            reverse("material-update", args=[self.material.id]),
            data={"consumed_quantity": "90.00", "remarks": "Updated after slab pour."},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["consumed_quantity"], "90.00")

    def test_custom_summary_links_project_and_materials(self):
        self.authenticate(self.engineer_token)
        response = self.client.get(
            reverse("project-materials-summary", kwargs={"code": self.project.code})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["project"]["code"], self.project.code)
        self.assertEqual(len(response.data["materials"]), 1)
        self.assertEqual(response.data["summary"]["material_entries"], 1)

