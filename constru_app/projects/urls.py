from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MaterialCreateAPIView,
    MaterialDetailAPIView,
    MaterialListAPIView,
    MaterialUpdateAPIView,
    ProjectCreateAPIView,
    ProjectDetailAPIView,
    ProjectListAPIView,
    ProjectUpdateAPIView,
    ProjectViewSet,
    project_materials_summary,
)

router = DefaultRouter()
router.register(r"projects/viewset", ProjectViewSet, basename="project-viewset")

urlpatterns = [
    path("", include(router.urls)),
    path("projects/list/", ProjectListAPIView.as_view(), name="project-list"),
    path("projects/create/", ProjectCreateAPIView.as_view(), name="project-create"),
    path("projects/<str:code>/detail/", ProjectDetailAPIView.as_view(), name="project-detail"),
    path("projects/<str:code>/update/", ProjectUpdateAPIView.as_view(), name="project-update"),
    path(
        "projects/<str:code>/materials-summary/",
        project_materials_summary,
        name="project-materials-summary",
    ),
    path("materials/list/", MaterialListAPIView.as_view(), name="material-list"),
    path("materials/create/", MaterialCreateAPIView.as_view(), name="material-create"),
    path("materials/<int:pk>/detail/", MaterialDetailAPIView.as_view(), name="material-detail"),
    path("materials/<int:pk>/update/", MaterialUpdateAPIView.as_view(), name="material-update"),
]

