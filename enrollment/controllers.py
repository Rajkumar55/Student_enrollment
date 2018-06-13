import base64

from django.contrib.auth.models import User
from enrollment.serializers import StudentProfileSerializer


def save_student_profile(data):
    try:
        profile_data = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'mobile_number': data.get('mobile_number', ''),
            'meta_data': {
                'email': data.get('email', '')
            }
        }

        serializer = StudentProfileSerializer(data=profile_data)
        is_valid = serializer.is_valid()
        if is_valid:
            password = base64.b64decode(data.get('password', ''))
            user = User.objects.create_user(data.get('email'), data.get('email'), password)
            profile_data['meta_data']['user_id'] = user
            profile = serializer.save()
            return True, profile
        return False, serializer.errors.get('meta_data') if serializer.errors.get('meta_data') else serializer.errors

    except Exception as e:
        return False, str(e)
