from rest_framework import serializers
from datetime import datetime
from enrollment.models import StudentProfile, Course, Enrollment


class StudentMetaSerializer(serializers.Serializer):
    user_id = serializers.RelatedField(allow_null=False, read_only=True)
    email = serializers.EmailField(max_length=75, allow_null=False, allow_blank=False, required=True,
                                   error_messages={'required': 'Email is required'})


class StudentProfileSerializer(serializers.Serializer):
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
    )
    first_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    mobile_number = serializers.CharField(max_length=15, allow_null=True, allow_blank=True)
    gender = serializers.ChoiceField(choices=GENDER, default=1)
    meta_data = StudentMetaSerializer()

    def create(self, validated_data):
        student_profile = StudentProfile()
        student_profile.user_id = self.initial_data['meta_data']['user_id']
        student_profile.first_name = self.initial_data.get('first_name', '')
        student_profile.last_name = self.initial_data.get('last_name', '')
        student_profile.email = self.initial_data['meta_data']['email']
        student_profile.mobile_number = self.initial_data.get('mobile_number', '')
        student_profile.gender = self.initial_data.get('gender', 1)
        student_profile.save()
        return student_profile


class CourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(required=True, max_length=50, allow_null=False, allow_blank=False)
    period = serializers.IntegerField(required=True, allow_null=False, help_text='Course Period In Months')
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        course = Course()
        course.course_name = self.initial_data.get('course_name', '')
        course.period = self.initial_data.get('period')
        course.is_active = self.initial_data.get('is_active')
        course.save()
        return course


class EnrollmentSerialzer(serializers.Serializer):
    course_id = serializers.RelatedField(allow_null=False, read_only=True)
    student_id = serializers.RelatedField(allow_null=False, read_only=True)

    def create(self, validated_data):
        enrollment = Enrollment()
        enrollment.course_id = self.initial_data.get('course_id')
        enrollment.student_id = self.initial_data.get('student_id')
        enrollment.save()
        return enrollment
