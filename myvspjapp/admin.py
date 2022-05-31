from django.contrib import admin
from myvspjapp.models import Faculty, Chair, Subject

# Register your models here.
@admin.register(Faculty)
class FaculyAdmin(admin.ModelAdmin):
    pass

@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass
