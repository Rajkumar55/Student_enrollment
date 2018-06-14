import base64

import binascii
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from enrollment.models import Course, StudentProfile, Enrollment
from enrollment.serializers import StudentProfileSerializer, EnrollmentSerialzer


def save_student_profile(data):
    try:
        gender = 1 if data.get('gender', 'male').lower() == 'male' else 2
        profile_data = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'mobile_number': data.get('mobile_number', ''),
            'gender': gender,
            'meta_data': {
                'email': data.get('email')
            }
        }

        serializer = StudentProfileSerializer(data=profile_data)
        is_valid = serializer.is_valid()
        if is_valid:
            password = base64.b64decode(data.get('password', ''))
            user = User.objects.create_user(data.get('email'), data.get('email'), password)
            token = Token.objects.create(user=user)
            profile_data['meta_data']['user_id'] = user
            profile = serializer.save()
            return True, token
        return False, serializer.errors.get('meta_data') if serializer.errors.get('meta_data') else serializer.errors

    except binascii.Error as be:
        return False, 'Password should be encoded in Base64 format'

    except Exception as e:
        return False, str(e)


def enroll_student(data):
    try:
        enrollment = Enrollment.objects.filter(course_id=data['course_id'])
        if len(enrollment) == 5:
            return False, 'Course completely booked'
        course = Course.objects.get(id=data['course_id'])
        student_profile = StudentProfile.objects.get(user_id=data['student_id'])
        enrollment_data = {
            'course_id': course,
            'student_id': student_profile
        }
        serializer = EnrollmentSerialzer(data=enrollment_data)
        is_valid = serializer.is_valid()
        if is_valid:
            serializer.save()
            return True, 'success'
        return False, serializer.errors

    except IntegrityError as ie:
        return False, 'Student already enrolled in the course'

    except Exception as e:
        return False, str(e)
