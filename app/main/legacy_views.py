from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {
        "title": "База учебных материалов",
        "username": "Иван Иванов",
        "role": "Студент",
    }
    return render(request, "index.html", context)


def login(request):
    context = {
        "title": "Авторизация",
    }
    return render(request, "login.html", context)


def registration(request):
    context = {
        "title": "Регистрация",
    }
    return render(request, "registration.html", context)


def favorites(request):
    context = {
        "title": "Избранное",
        "username": "Иван Иванов",
        "role": "Студент",
        "facultet": "ИУ",
        "cafedra": "ИУ-5",
        "semester": "1",
        "lesson": "Дискретная математика",
        "filename": "Методичка"
    }
    return render(request, "favorites.html", context)


def search(request):
    context = {
        "title": "Поиск",
    }
    return render(request, "search.html", context)


def storage(request):
    context = {
        "title": "Хранилище",
    }
    return render(request, "storage.html", context)


def files(request):
    context = {
        "title": "Файлы",
    }
    return render(request, "files.html", context)


def load(request):
    context = {
        "title": "Загрузить файл",
    }
    return render(request, "load.html", context)


