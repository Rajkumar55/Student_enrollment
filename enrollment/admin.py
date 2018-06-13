from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from enrollment.models import StudentProfile


class StudentProfileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    list_display = ['user_id', 'first_name', 'last_name', 'email', 'mobile_number', 'created_date']
    search_fields = ['mobile_number', 'email', 'first_name', 'last_name']
    list_display_links = ['user_id']
    raw_id_fields = ('user_id',)

admin.site.register(StudentProfile, StudentProfileAdmin)
