import base64
import json

import binascii
from django.contrib import auth
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from enrollment.controllers import save_student_profile, enroll_student, leave_course
from enrollment.models import Course, StudentProfile
from enrollment.serializers import CourseSerializer, StudentProfileSerializer


class RegistrationView(viewsets.ModelViewSet):
    model = StudentProfile
    serializer_class = StudentProfileSerializer
    queryset = model.objects.all()

    def list(self, request, *args, **kwargs):
        # queryset = self.model.objects.all()
        serializer = StudentProfileSerializer(self.queryset, many=True)
        response = {
            'status': 'success',
            'data': serializer.data
        }
        return JsonResponse(response)

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        is_registered, result = save_student_profile(data)
        if is_registered:
            user = auth.authenticate(username=data['email'], password=data['password'])
            auth.login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Student registered successfully',
                                 'access_token': result.key})
        error_message = {
            'status': 'fail',
            'message': result
        }
        return JsonResponse(error_message, status=400)


def register(request):
    data = json.loads(request.body)
    is_registered, result = save_student_profile(data)
    if is_registered:
        user = auth.authenticate(username=data['email'], password=data['password'])
        auth.login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Student registered successfully'})
    error_message = {
        'status': 'fail',
        'message': result
    }
    return JsonResponse(error_message, status=400)


def login(request):
    data = json.loads(request.body)
    # try:
    user = auth.authenticate(username=data['email'], password=data['password'])
    if user is not None:
        if user.is_active:
            # request.session.set_expiry(60)  # sets the exp. value of the session
            auth.login(request, user)
            return JsonResponse({'status': 'success', 'messgae': 'Logged in successful'})
    return JsonResponse({'status': 'fail', 'messgae': 'Unable to Login. Please check the email or password'})
    # except binascii.Error as be:
    #     return JsonResponse({'status': 'fail', 'messgae': 'Password should be encoded in Base64 format'})


def logout(request):
    if request.user.is_authenticated:
        print(request.user)
        auth.logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
    return JsonResponse({'status': 'fail', 'message': 'You need to login first'})


def reset_password(request):
    if request.user.is_authenticated and not request.user.is_staff:
        data = json.loads(request.body)
        if not data.get('email', ''):
            return JsonResponse({'status': 'fail', 'message': 'Enter a valid email'})
        elif not data.get('new_password', ''):
            return JsonResponse({'status': 'fail', 'message': 'New password not available'})
        user = auth.authenticate(username=data['email'], password=data.get('old_password', ''))
        if user is not None:
            user.set_password(data['new_password'])
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Password updated'})
        return JsonResponse({'status': 'fail', 'message': 'Unable to Login. Please check the email or old password'})
    return JsonResponse({'status': 'fail', 'message': 'Not authorized to change password'})


class CourseView(viewsets.ModelViewSet):
    model = Course
    serializer_class = CourseSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            print(request.session)
            queryset = self.model.objects.filter(is_active=True)
            serializer = CourseSerializer(queryset, many=True)
            response = {
                'status': 'success',
                'data': serializer.data
            }
            return JsonResponse(response)
        else:
            error_responsse = {'status': 'fail', 'message': 'You need to Login first'}
            return JsonResponse(error_responsse)


def enroll(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        # token = request.META['HTTP_AUTHORIZATION']
        body = json.loads(request.body)
        data = {
            'course_id': body.get('course_id'),
            'student_id': user
        }
        enrolled, data = enroll_student(data)
        if enrolled:
            response = {
                'status': 'success',
                'message': 'Student Enrolled in the course'
            }
            return JsonResponse(response)
        error_response = {
            'status': 'fail',
            'message': data
        }
        return JsonResponse(error_response, status=400)
    else:
        error_responsse = {'status': 'fail', 'message': 'You need to Login first'}
        return JsonResponse(error_responsse)


def leave(request):
    if request.user.is_authenticated:
        user = request.user
        body = json.loads(request.body)
        data = {
            'course_id': body.get('course_id'),
            'student_id': user
        }
        left, data = leave_course(data)
        if left:
            response = {
                'status': 'success',
                'message': 'Student left the course'
            }
            return JsonResponse(response)
        error_response = {
            'status': 'fail',
            'message': data
        }
        return JsonResponse(error_response, status=400)
    else:
        error_responsse = {'status': 'fail', 'message': 'You need to Login first'}
        return JsonResponse(error_responsse)
