from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from app.main.forms import SignUpForm, SignInForm, FileUploadForm, DepartmentForm, SpecializationForm, CourseForm, \
    FileTypeForm, CourseDisciplineForm
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

    def filter_queryset(self, queryset):
        if not self.request.GET.get('q', ''):
            return self.queryset.none()
        return queryset.filter(title__contains=self.request.GET.get('q', ''))

    def get_queryset(self):
        qs = self.queryset
        extra_filter = {}
        if self.request.GET.get('typeFilter'):
            extra_filter['type'] = self.request.GET['typeFilter']

        if self.request.GET.get('blockFilter'):
            extra_filter['course_discipline'] = self.request.GET['blockFilter']
        return self.filter_queryset(qs.filter(**extra_filter))

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['query'] = self.request.GET.get('q', '')
        data['title'] = "Результаты поиска"
        return data


class AllFiles(Search):
    template_name = 'search.html'
    queryset = Document.objects.all()

    def filter_queryset(self, queryset):
        return queryset

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['query'] = None
        data['title'] = "Все файлы"
        return data


class Storage(LoginRequired, DetailView):
    template_name = 'storage.html'
    queryset = Department.objects

    def get_context_data(self, **kwargs):
        return {
            'specialization_list': self.object.specialization_set.all().order_by('title'),
            'title': "Кафедры и предметы факультета {}".format(self.object)
        }


class CourseDetail(LoginRequired, DetailView):
    template_name = 'files.html'
    queryset = Course.objects

    def get_context_data(self, **kwargs):
        extra_filter = {}
        if self.request.GET.get('typeFilter'):
            extra_filter['type'] = self.request.GET['typeFilter']

        if self.request.GET.get('blockFilter'):
            extra_filter['course_discipline'] = self.request.GET['blockFilter']
        return {
            'object': self.object,
            'course': self.object,
            'document_list': Document.objects.filter(course_discipline__course=self.object, **extra_filter),
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


class FavoritesAddDiscipline(View):
    def get(self, request):
        disc_id = self.request.GET['disc_id']
        if not request.user.is_authenticated or not disc_id:
            return HttpResponseForbidden()
        documents = Document.objects.filter(course_discipline__id=disc_id)
        for d in documents:
            request.user.favorites.add(d)
        return JsonResponse({}, status=200)


class AddView(TemplateView):
    template_name = 'add_choice.html'
    form = None
    success_action_text = 'добавлен'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.groups.first().name != 'Преподаватели':
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'action': self.request.path,
            'title': 'Добавить',
            'dform': DepartmentForm(),
            'sform': SpecializationForm(),
            'cform': CourseForm(),
            'tform': FileTypeForm(),
            'cdform': CourseDisciplineForm(),
        }

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        context = self.get_context_data()
        for key, value in context.items():
            if isinstance(value, self.form):
                form.active = True
                context[key] = form
        if form.is_valid():
            form.save()
        return self.render_to_response(context)


class FileUpload(TemplateView):
    template_name = 'load.html'
    form = FileUploadForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.groups.first().name != 'Преподаватели':
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'title': 'Загрузить файл',
            'form': self.form
        }

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(False)
            doc.author = request.user
            doc.save()
            return self.render_to_response({'form': form, 'success': True})
        return self.render_to_response({'form': form})


class AddDepartment(AddView):
    form = DepartmentForm


class AddSpecialization(AddView):
    form = SpecializationForm


class AddCourse(AddView):
    form = CourseForm


class AddCourseDiscipline(AddView):
    form = CourseDisciplineForm


class AddFileType(AddView):
    form = FileTypeForm
