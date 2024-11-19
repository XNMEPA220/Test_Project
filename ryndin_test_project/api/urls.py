from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DivisionViewSet, EmployeeViewSet, PermissionsViewSet, PostViewSet

app_name = 'api'
router = DefaultRouter()

router.register(
    'divisions',
    DivisionViewSet,
    basename='divisions'
)
router.register(
    'posts',
    PostViewSet,
    basename='posts'
)
router.register(
    'permissions',
    PermissionsViewSet,
    basename='permissions'
)

router.register(
    'employees',
    EmployeeViewSet,
    basename='employees'
)

urlpatterns = [
    path('', include(router.urls)),
]
