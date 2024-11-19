from django.db import models


class Division(models.Model):
    """Модель подразделения."""
    name = models.CharField('Название подразделения', max_length=100)
    main_division = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='main_divisions',
        blank=True,
        null=True
    )
    posts = models.ManyToManyField(
        'Post',
        through='DivisionPost',
        related_name='divisions'
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель должности."""
    name = models.CharField('Название должности', max_length=100)
    permissions = models.ManyToManyField(
        'Permissions',
        through='PostPermissions',
        related_name='permissions'
    )

    def __str__(self):
        return self.name


class Permissions(models.Model):
    """"Модель права."""
    name = models.CharField('Название права', max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Модель сотрудника."""
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100)
    posts = models.ManyToManyField(
        Post,
        through='EmployeePost',
        related_name='employees'
    )


class PostPermissions(models.Model):
    """Модель связи должности и прав."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_permissions'
    )
    permissions = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE,
        related_name='permission'
    )

    def __str__(self):
        return f'{self.permissions} принадлежащее {self.post}'


class DivisionPost(models.Model):
    """Модель связи подразделения и должности."""
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        related_name='division_post'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_division'
    )


class EmployeePost(models.Model):
    """""Модель связи сотрудника и должности."""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employee_post'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_employee'
    )
