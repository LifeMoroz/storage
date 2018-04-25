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
    image = models.ImageField('Картинка', null=True, blank=True)
    department = models.ForeignKey(Department, models.CASCADE, verbose_name='Факультет')

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедра'

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField('Название', max_length=255)
    specialization = models.ForeignKey(Specialization, models.CASCADE, verbose_name='Кафедра')
    image = models.ImageField('Картинка', null=True, blank=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return "{}/{}".format(self.specialization, self.title)


class Type(models.Model):
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип файла'
        verbose_name_plural = 'Типы файлов'


class Document(models.Model):
    title = models.CharField('Название', max_length=255)
    file = models.FileField(verbose_name='Файл')
    # TYPE_CHOICES = ((1, 'Шаблон работы'), (2, 'Методичекие указания'), (3, 'Видеофайл'), (4, 'Домашнее задание'))
    # type = models.IntegerField(verbose_name='Тип файла', choices=TYPE_CHOICES)
    type = models.ForeignKey(Type, models.CASCADE, verbose_name='Тип файла')
    author = models.ForeignKey(User, models.CASCADE, verbose_name='Автор')
    course = models.ForeignKey(Course, models.CASCADE, verbose_name='Предмет')
    created = models.DateTimeField(verbose_name='Создано', default=timezone.now, editable=False)
    users = models.ManyToManyField(User, related_name='favorites')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
