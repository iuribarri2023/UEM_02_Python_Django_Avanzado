from rest_framework.permissions import BasePermission, DjangoModelPermissions


ENGINEERS_GROUP = "Engineers"
WORKERS_GROUP = "Workers"
ALLOWED_GROUPS = (ENGINEERS_GROUP, WORKERS_GROUP)


class GroupModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if not user.groups.filter(name__in=ALLOWED_GROUPS).exists():
            return False
        return super().has_permission(request, view)


class ProjectMaterialsSummaryPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if not user.groups.filter(name__in=ALLOWED_GROUPS).exists():
            return False
        return (
            user.has_perm("projects.view_constructionproject")
            and user.has_perm("projects.view_projectmaterial")
        )

