from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='static/img/users', verbose_name='Аватар', blank=True)


class Department(models.Model):
    code = models.TextField(max_length=5, verbose_name='Код')
    full_name = models.TextField(verbose_name='Полное название')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'


class Teacher(models.Model):
    first_name = models.TextField(verbose_name='Имя')
    patronymic = models.TextField(verbose_name='Отчество', default=None, blank=True, null=True)
    last_name = models.TextField(verbose_name='Фамилия')
    department = models.ForeignKey(Department, verbose_name='Кафедра', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='static/img/teachers', default=None, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Subject(models.Model):
    name = models.TextField(verbose_name='Название')
    semester = models.IntegerField(verbose_name='Семестр')
    teachers = models.ManyToManyField(Teacher, verbose_name='Преподаватели', related_name='subjects', blank=True)
    default_department = models.ForeignKey(Department, verbose_name='Кафедра по умолч.', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Like(models.Model):
    teacher = models.ForeignKey(Teacher, verbose_name='Кого лайкнули', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Кто лайкнул', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'{self.user.username} оценил {self.teacher.first_name} {self.teacher.last_name}'
