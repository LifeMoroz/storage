from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from app.main.forms import SignUpForm, SignInForm, FileUploadForm
from app.main.models import Department, Document, Course


class LoginRequired:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:signin')
        return super().dispatch(request, *args, **kwargs)


class SignOut(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main:index')


class SignUp(TemplateView):
    template_name = 'auth/signup.html'

    def get_context_data(self, **kwargs):
        return {'form': SignUpForm()}

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            login(request, user)
            return redirect('main:index')
        return self.render_to_response({'form': form})


class SignIn(TemplateView):
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        return {'form': SignInForm()}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = SignInForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if not user or not check_password(password, user.password):
                form.add_error(NON_FIELD_ERRORS, 'Ошибка авторизации')
                return self.render_to_response({'form': form})

            login(request, user)
            return redirect('main:index')

        return self.render_to_response({'form': form})


class Index(LoginRequired, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {
            'object_list': Department.objects.all(),
            'title': "База учебных материалов МГТУ им.Баумана"
        }


class Search(LoginRequired, ListView):
    template_name = 'search.html'
    queryset = Document.objects

    def get_queryset(self):
        return self.queryset.filter(title__contains=self.request.GET.get('q', ''))

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['query'] = self.request.GET.get('q', '')
        data['title'] = "Результаты поиска"
        return data


class Storage(LoginRequired, DetailView):
    template_name = 'storage.html'
    queryset = Department.objects

    def get_context_data(self, **kwargs):
        return {
            'specialization_list': self.object.specialization_set.all(),
            'title': "Кафедры и предметы факультета {}".format(self.object)
        }


class CourseDetail(LoginRequired, DetailView):
    template_name = 'files.html'
    queryset = Course.objects

    def get_context_data(self, **kwargs):
        return {
            'object': self.object,
            'document_list': Document.objects.filter(course=self.object),
            'title': "Файлы факультета {}".format(self.object)
        }


class Favorites(LoginRequired, ListView):
    template_name = 'favorites.html'

    def get_queryset(self):
        return self.request.user.favorites.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = "Избранное"
        return data


class FavoritesRemove(View):
    def get(self, request, document_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise Http404
        request.user.favorites.remove(document)
        return JsonResponse({}, status=200)


class FavoritesAdd(View):
    def get(self, request, document_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise Http404
        request.user.favorites.add(document)
        return JsonResponse({}, status=200)


class FileUpload(TemplateView):
    template_name = 'load.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.groups.first().name != 'Преподаватели':
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {'form': FileUploadForm()}

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(False)
            doc.author = request.user
            doc.save()
            return self.render_to_response({'form': form, 'success': True})
        return self.render_to_response({'form': form})
