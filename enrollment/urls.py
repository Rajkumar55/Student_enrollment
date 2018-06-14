from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from enrollment.views import CourseView, enroll_student_view

course_view = CourseView.as_view({
    'get': 'list'
})
urlpatterns = [
    path('list/', course_view),
    path('enroll/', csrf_exempt(enroll_student_view))
    # path('enroll/', csrf_exempt(EnrollmentView.as_view()))
]
