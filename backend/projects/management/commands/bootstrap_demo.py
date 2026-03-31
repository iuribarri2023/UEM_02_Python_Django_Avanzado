from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from projects.models import ConstructionProject, ProjectMaterial
from projects.permissions import ENGINEERS_GROUP, WORKERS_GROUP


class Command(BaseCommand):
    help = 'Creates demo users, tokens and sample construction data for local testing.'

    def handle(self, *args, **options):
        engineers_group = Group.objects.get(name=ENGINEERS_GROUP)
        workers_group = Group.objects.get(name=WORKERS_GROUP)

        engineer, engineer_created = User.objects.get_or_create(username='engineer')
        engineer.set_password('engineer123')
        engineer.is_staff = False
        engineer.is_superuser = False
        engineer.save()
        engineer.groups.set([engineers_group])
        engineer_token, _ = Token.objects.get_or_create(user=engineer)

        worker, worker_created = User.objects.get_or_create(username='worker')
        worker.set_password('worker123')
        worker.is_staff = False
        worker.is_superuser = False
        worker.save()
        worker.groups.set([workers_group])
        worker_token, _ = Token.objects.get_or_create(user=worker)

        project, project_created = ConstructionProject.objects.update_or_create(
            code='OBR-001',
            defaults={
                'name': 'Residential Tower Aravaca',
                'project_type': ConstructionProject.ProjectType.RESIDENTIAL,
                'client_name': 'Habitat Europa',
                'site_address': 'Avenida de la Obra 14',
                'city': 'Madrid',
                'project_manager': 'Laura Torres',
                'engineer_in_charge': 'Carlos Mendez',
                'contract_reference': 'CTR-ARV-2026-01',
                'start_date': '2026-04-01',
                'expected_end_date': '2027-03-31',
                'budget': '2750000.00',
                'status': ConstructionProject.Status.EXECUTION,
                'progress_percentage': 18,
                'notes': 'Foundation and retaining walls in progress.',
            },
        )

        material, material_created = ProjectMaterial.objects.update_or_create(
            project=project,
            delivery_note='ALB-0001',
            defaults={
                'category': ProjectMaterial.Category.STRUCTURE,
                'material_name': 'HA-25 concrete',
                'supplier': 'Hormigones Centro',
                'batch_reference': 'LOT-HA25-APR',
                'storage_zone': 'North silo',
                'received_by': 'Miguel Ruiz',
                'unit': ProjectMaterial.Unit.M3,
                'planned_quantity': '180.00',
                'received_quantity': '110.00',
                'consumed_quantity': '75.00',
                'unit_cost': '92.50',
                'received_on': '2026-04-10',
                'quality_checked': True,
                'remarks': 'Delivery accepted after slump test.',
            },
        )

        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write(f'Engineer user: engineer / engineer123 | Token: {engineer_token.key}')
        self.stdout.write(f'Worker user: worker / worker123 | Token: {worker_token.key}')
        self.stdout.write(
            f'Project: {project.code} (created={project_created}) | Material id: {material.id} (created={material_created})'
        )
        self.stdout.write(
            f'Users created: engineer={engineer_created}, worker={worker_created}'
        )
