from rest_framework import serializers

from enrollment.models import StudentProfile

class StudentMetaSerializer(serializers.Serializer):
    user_id = serializers.RelatedField(allow_null=False, read_only=True)
    email = serializers.EmailField(max_length=75, allow_null=False, allow_blank=False, required=True)


class StudentProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    mobile_number = serializers.CharField(max_length=15, allow_null=True, allow_blank=True)
    meta_data = StudentMetaSerializer()

    def create(self, validated_data):
        student_profile = StudentProfile()
        student_profile.user_id = self.initial_data['meta_data']['user_id']
        student_profile.first_name = self.initial_data.get('first_name', '')
        student_profile.last_name = self.initial_data.get('last_name', '')
        student_profile.email = self.initial_data['meta_data']['email']
        student_profile.mobile_number = self.initial_data.get('mobile_number', '')
        student_profile.save()
        return student_profile
