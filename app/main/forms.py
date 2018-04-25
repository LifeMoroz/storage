from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ImproperlyConfigured

from app.main.constants import Position
from app.main.models import Document, Course, Type


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
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label='Предмет',
        widget=forms.widgets.Select(attrs={'class': 'custom-select'})
    )

    class Meta:
        model = Document
        exclude = ('users', 'author')
