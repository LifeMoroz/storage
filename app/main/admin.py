from django.contrib import admin


# Register your models here.
from app.main.models import Document, Course, Specialization, Department, Type, CourseDiscipline


class DepartmentAdmin(admin.ModelAdmin):
    pass


class SpecializationAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class TypeAdmin(admin.ModelAdmin):
    pass


class DocumentAdmin(admin.ModelAdmin):
    exclude = ('users',)


class CourseDisciplineAdmin(admin.ModelAdmin):
    pass


admin.site.register(Type, TypeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseDiscipline, CourseDisciplineAdmin)
admin.site.register(Document, DocumentAdmin)
