from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from enrollment.models import StudentProfile, Course, Enrollment


class StudentProfileAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):

    list_display = ['user_id', 'first_name', 'last_name', 'email', 'mobile_number', 'gender', 'created_date']
    search_fields = ['mobile_number', 'email', 'first_name', 'last_name']
    list_display_links = ['user_id']
    raw_id_fields = ('user_id',)

admin.site.register(StudentProfile, StudentProfileAdmin)


@admin.register(Course)
class CourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'course_name', 'period', 'is_active', 'created_date']
    search_fields = ['course_name']
    list_filter = ['is_active']


@admin.register(Enrollment)
class EnrollmentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'course_id', 'student_id', 'created_date']
    list_filter = ['course_id', 'student_id']
    raw_id_fields = ('course_id', 'student_id',)
