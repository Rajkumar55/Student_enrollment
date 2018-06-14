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

from enrollment.controllers import save_student_profile, enroll_student
from enrollment.models import Course, StudentProfile
from enrollment.serializers import CourseSerializer, StudentProfileSerializer


class RegistrationView(viewsets.ModelViewSet):
    model = StudentProfile
    serializer_class = StudentProfileSerializer
    queryset = model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        serializer = StudentProfileSerializer(queryset, many=True)
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
            user = auth.authenticate(username=data['email'], password=base64.b64decode(data['password']))
            auth.login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Student registered successfully',
                                 'access_token': result.key})
        error_message = {
            'status': 'fail',
            'message': result
        }
        return JsonResponse(error_message, status=400)


def login(request):
    data = json.loads(request.body)
    try:
        user = auth.authenticate(username=data['email'], password=base64.b64decode(data['password']))
        if user is not None:
            if user.is_active:
                # request.session.set_expiry(60)  # sets the exp. value of the session
                auth.login(request, user)
                return JsonResponse({'status': 'success', 'messgae': 'Logged in successful'})
        return JsonResponse({'status': 'fail', 'messgae': 'Unable to Login. Please check the username or password'})
    except binascii.Error as be:
        return JsonResponse({'status': 'fail', 'messgae': 'Password should be encoded in Base64 format'})


def logout(request):
    if request.user.is_authenticated:
        print(request.user)
        auth.logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
    return JsonResponse({'status': 'fail', 'message': 'You need to login first'})


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


# class EnrollmentView(generics.CreateAPIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
#     # permission_classes = (IsAuthenticated,)

def enroll_student_view(request):#(self, request, **kwargs):
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
