from rest_framework import serializers

from .models import Division, DivisionPost, Employee, EmployeePost, Permissions, Post, PostPermissions


class PostPermissionsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи между должностью и правом."""
    name = serializers.StringRelatedField(
        source='permissions.name'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='permissions',
        queryset=Permissions.objects.all()
    )

    class Meta:
        model = PostPermissions
        fields = (
            'id',
            'name'
        )


class DivisionPostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи между подразделением и должностью."""
    name = serializers.StringRelatedField(
        source='post.name'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='post',
        queryset=Post.objects.all()
    )

    class Meta:
        model = DivisionPost
        fields = (
            'id',
            'name'
        )


class DivisionSerializer(serializers.ModelSerializer):
    """"Сериализатор для модели подразделения."""
    post = serializers.SerializerMethodField()
    subdivision = serializers.SerializerMethodField()

    def get_post(self, obj):
        post = DivisionPost.objects.filter(division=obj)
        return DivisionPostSerializer(post, many=True).data

    def get_subdivision(self, obj):
        subdivision = Division.objects.filter(main_division=obj)
        return DivisionSerializer(subdivision, many=True).data

    class Meta:
        model = Division
        fields = (
            'id',
            'name',
            'post',
            'main_division',
            'subdivision'
        )


class PostSerializer(serializers.ModelSerializer):
    """""Сериализатор для модели должности."""
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        permissions = PostPermissions.objects.filter(post=obj)
        return PostPermissionsSerializer(permissions, many=True).data

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'permissions'
        )


class PermissionsSerializer(serializers.ModelSerializer):
    """""Сериализатор для модели прав."""

    class Meta:
        model = Permissions
        fields = '__all__'


class CreatePostInDivisionSerializer(serializers.ModelSerializer):
    """Сериализатор для создания должности в подразделении."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
    )

    class Meta:
        model = DivisionPost
        fields = ('id',)


class BaseCreateSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для создания объекта со связанным объектом."""

    @staticmethod
    def bulk_create_related(parent, items, relation_class, parent_field, item_field, item_slice):
        create_items = [
            relation_class(
                **{parent_field: parent},
                **{item_field: item[item_slice]},
            )
            for item in items
        ]
        relation_class.objects.bulk_create(create_items)

    def create(self, validated_data):
        related_items = validated_data.pop(self.related_field_name)
        instance = self.Meta.model.objects.create(**validated_data)
        self.bulk_create_related(
            instance,
            related_items,
            self.relation_class,
            self.parent_field_name,
            self.item_field_name,
            self.item_slice_name
        )
        return instance

    def update(self, instance, validated_data):
        related_items = validated_data.pop(self.related_field_name, None)
        if related_items:
            getattr(instance, self.related_field_name).clear()
        self.bulk_create_related(
            instance,
            related_items,
            self.relation_class,
            self.parent_field_name,
            self.item_field_name
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = self.base_serializer(
            instance,
            context={'requeest': self.context['request']}
        )
        return serializer.data


class CreatePermissionsInPostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания прав в должности."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Permissions.objects.all(),
        source='permission',
    )

    class Meta:
        model = PostPermissions
        fields = ('id',)


class EmployeePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи должности и сотрудника."""
    name = serializers.StringRelatedField(
        source='post.name'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='post',
        queryset=Post.objects.all()
    )
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        permissions = PostPermissions.objects.filter(post=obj.post)
        return PostPermissionsSerializer(permissions, many=True).data

    class Meta:
        model = EmployeePost
        fields = (
            'id',
            'name',
            'permissions'
        )


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели сотрудника."""
    post = serializers.SerializerMethodField()

    def get_post(self, obj):
        post = EmployeePost.objects.filter(employee=obj)
        return EmployeePostSerializer(post, many=True).data

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'surname',
            'patronymic',
            'post'
        )


class CreatePostInEmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания должности для сотрудника."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
    )

    class Meta:
        model = EmployeePost
        fields = ('id',)


class EmployeeCreateSerializer(BaseCreateSerializer, EmployeeSerializer):
    """Сериализатор для создания сотрудника."""
    posts = CreatePostInEmployeeSerializer(many=True)
    related_field_name = 'posts'
    relation_class = EmployeePost
    parent_field_name = 'employee'
    item_field_name = 'post'
    item_slice_name = 'post'
    base_serializer = EmployeeSerializer

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'surname',
            'patronymic',
            'posts'
        )


class PostCreateSerializer(BaseCreateSerializer, PostSerializer):
    """"Сериализатор для создания должности."""
    permissions = CreatePermissionsInPostSerializer(many=True)
    related_field_name = 'permissions'
    relation_class = PostPermissions
    parent_field_name = 'post'
    item_field_name = 'permissions'
    item_slice_name = 'permission'
    base_serializer = PostSerializer

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'permissions'
        )


class DivisionCreateSerializer(BaseCreateSerializer, DivisionSerializer):
    """Сериализатор для создания подразделения."""
    posts = CreatePostInDivisionSerializer(many=True)
    main_division = serializers.PrimaryKeyRelatedField(
        queryset=Division.objects.all(),
        required=False
    )

    related_field_name = 'posts'
    relation_class = DivisionPost
    parent_field_name = 'division'
    item_field_name = 'post'
    item_slice_name = 'post'
    base_serializer = DivisionSerializer

    class Meta:
        model = Division
        fields = (
            'id',
            'name',
            'posts',
            'main_division'
        )
