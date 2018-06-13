import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from enrollment.controllers import save_student_profile


class RegistrationView(viewsets.ModelViewSet):
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        is_registered, data = save_student_profile(data)
        if is_registered:
            return JsonResponse({'status': 'success', 'message': 'Student registered successfully'})
        error_message = {
            'status': 'fail',
            'message': str(data)
        }
        return JsonResponse(error_message)
