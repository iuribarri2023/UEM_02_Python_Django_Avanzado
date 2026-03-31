from django.db import migrations


ENGINEERS_GROUP = "Engineers"
WORKERS_GROUP = "Workers"


def create_groups_and_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    project_content_type, _ = ContentType.objects.get_or_create(
        app_label="projects",
        model="constructionproject",
    )
    material_content_type, _ = ContentType.objects.get_or_create(
        app_label="projects",
        model="projectmaterial",
    )

    permission_specs = {
        project_content_type: [
            ("add_constructionproject", "Can add construction project"),
            ("change_constructionproject", "Can change construction project"),
            ("delete_constructionproject", "Can delete construction project"),
            ("view_constructionproject", "Can view construction project"),
        ],
        material_content_type: [
            ("add_projectmaterial", "Can add project material"),
            ("change_projectmaterial", "Can change project material"),
            ("delete_projectmaterial", "Can delete project material"),
            ("view_projectmaterial", "Can view project material"),
        ],
    }

    created_permissions = {}
    for content_type, specs in permission_specs.items():
        for codename, name in specs:
            permission, _ = Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={"name": name},
            )
            created_permissions[codename] = permission

    engineers_group, _ = Group.objects.get_or_create(name=ENGINEERS_GROUP)
    workers_group, _ = Group.objects.get_or_create(name=WORKERS_GROUP)

    engineers_group.permissions.set(
        [
            created_permissions["add_constructionproject"],
            created_permissions["change_constructionproject"],
            created_permissions["delete_constructionproject"],
            created_permissions["view_constructionproject"],
            created_permissions["add_projectmaterial"],
            created_permissions["change_projectmaterial"],
            created_permissions["delete_projectmaterial"],
            created_permissions["view_projectmaterial"],
        ]
    )

    workers_group.permissions.set(
        [
            created_permissions["view_constructionproject"],
            created_permissions["view_projectmaterial"],
            created_permissions["add_projectmaterial"],
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, migrations.RunPython.noop),
    ]
