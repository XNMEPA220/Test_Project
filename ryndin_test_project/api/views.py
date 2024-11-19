from rest_framework import viewsets

from .models import Division, Employee, Permissions, Post
from .serializers import DivisionCreateSerializer, DivisionSerializer, EmployeeCreateSerializer, EmployeeSerializer, \
    PermissionsSerializer, PostCreateSerializer, PostSerializer


class DivisionViewSet(viewsets.ModelViewSet):
    """Представление для модели подразделений."""
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return DivisionSerializer
        return DivisionCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Представление для модели должностей."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PostSerializer
        return PostCreateSerializer


class PermissionsViewSet(viewsets.ModelViewSet):
    """Представление для модели прав."""
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """Представление для модели сотрудников."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return EmployeeSerializer
        return EmployeeCreateSerializer
