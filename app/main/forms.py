from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.functional import SimpleLazyObject

from app.main.constants import Position
from app.main.models import Document, Course, Type, Department, Specialization, CourseDiscipline


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите имя'}),
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите фамилию'}),
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите email'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль ещё раз'}),
    )
    position = forms.ChoiceField(
        label='Должность',
        choices=((Position.TEACHER, 'Преподаватель'), (Position.STUDENT, 'Студент'))
    )

    def clean_position(self):
        self.cleaned_data['position'] = int(self.cleaned_data['position'])
        return self.cleaned_data['position']

    def save(self, commit=True):
        user = super().save(True)
        if self.cleaned_data['position'] == Position.TEACHER:
            user.groups.add(Group.objects.get(name='Преподаватели'))
        elif self.cleaned_data['position'] == Position.STUDENT:
            user.groups.add(Group.objects.get(name='Студенты'))
        else:
            user.delete()
            raise ImproperlyConfigured('Unsupported group')
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'position', 'password1', 'password2')


class SignInForm(forms.ModelForm):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите email'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Введите пароль'}),
    )

    class Meta:
        model = User
        fields = ('email', 'password')


class FileUploadForm(forms.ModelForm):
    title = forms.CharField(
        label='Название файла',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label='Тип файла',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'}),
    )
    course_discipline = forms.ModelChoiceField(
        queryset=CourseDiscipline.objects.all(),
        label='Учебный блок',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'})
    )

    class Meta:
        model = Document
        exclude = ('users', 'author')


class DepartmentForm(forms.ModelForm):

    title = forms.CharField(
        label='Название факультета',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )

    class Meta:
        model = Department
        fields = ('title', 'image')
        action = 'main:add-department'
        success_action_text = '{} добавлен'.format(model._meta.verbose_name)


class SpecializationForm(forms.ModelForm):

    title = forms.CharField(
        label='Название кафедры',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label='Факультет',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'})
    )

    class Meta:
        model = Specialization
        fields = ('title', 'department')
        action = 'main:add-specialization'
        success_action_text = '{} добавлена'.format(model._meta.verbose_name)


class CourseForm(forms.ModelForm):

    title = forms.CharField(
        label='Название учебной дисциплины',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        label='Кафедра',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'})
    )

    class Meta:
        model = Course
        fields = ('title', 'specialization')
        action = 'main:add-course'
        success_action_text = '{} добавлена'.format(model._meta.verbose_name)


class CourseDisciplineForm(forms.ModelForm):

    title = forms.CharField(
        label='Название учебного блока',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label='Учебная дисциплина',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'})
    )

    class Meta:
        model = CourseDiscipline
        fields = ('title', 'course')
        action = 'main:add-course-discipline'
        success_action_text = '{} добавлен'.format(model._meta.verbose_name)


class FileTypeForm(forms.ModelForm):

    title = forms.CharField(
        label='Название типа файла',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите название'}),
    )

    class Meta:
        model = Type
        fields = ('title',)
        action = 'main:add-file-type'
        success_action_text = '{} добавлен'.format(model._meta.verbose_name)
