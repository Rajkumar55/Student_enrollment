from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=75, null=False, blank=False, db_index=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'student_profile'


class Course(models.Model):
    course_name = models.CharField(max_length=100, null=False, blank=False)
    period = models.IntegerField(null=False, blank=False, help_text='Course Period In Months')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'courses'


class Enrollment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_id')
    student_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enrollment'
        unique_together = (('course_id', 'student_id'),)
