from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Department(models.Model):
    title = models.CharField('Название', max_length=255)
    image = models.ImageField('Картинка')

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:storage', args=(self.id,))


class Specialization(models.Model):
    title = models.CharField('Название', max_length=255)
    department = models.ForeignKey(Department, models.CASCADE, verbose_name='Факультет')

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедра'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField('Название', max_length=255)
    specialization = models.ForeignKey(Specialization, models.CASCADE, verbose_name='Кафедра')

    class Meta:
        verbose_name = 'Учебная дисциплина'
        verbose_name_plural = 'Учебные дисциплины'
        ordering = ('title',)

    def __str__(self):
        return "{}/{}".format(self.specialization, self.title)


class Type(models.Model):
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип файла'
        verbose_name_plural = 'Типы файлов'
        ordering = ('title',)


class CourseDiscipline(models.Model):
    title = models.CharField('Название', max_length=255)
    course = models.ForeignKey(Course, models.CASCADE)

    def __str__(self):
        return str(self.course) + ' - ' + str(self.title)

    class Meta:
        verbose_name = 'Учебный блок'
        verbose_name_plural = 'Файлы'
        ordering = ('course__title', 'title',)


class Document(models.Model):
    title = models.CharField('Название', max_length=255)
    file = models.FileField(verbose_name='Файл')
    type = models.ForeignKey(Type, models.CASCADE, verbose_name='Тип файла')
    author = models.ForeignKey(User, models.CASCADE, verbose_name='Автор')
    course_discipline = models.ForeignKey(CourseDiscipline, models.CASCADE, verbose_name='Предмет', null=True)
    created = models.DateTimeField(verbose_name='Создано', default=timezone.now, editable=False)
    users = models.ManyToManyField(User, related_name='favorites')

    def __str__(self):
        return self.title

    @property
    def course(self):
        if self.course_discipline:
            return self.course_discipline.course
        return None

    @property
    def size(self):
        if self.file:
            return round(self.file.size * 1. / 1000, 1)
        return '-'

    @property
    def extension(self):
        if self.file:
            return self.file.path.split('.')[-1]
        return '-'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ('course_discipline__title', 'title',)
