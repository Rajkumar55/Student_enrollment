from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from enrollment.views import CourseView, enroll, leave

course_view = CourseView.as_view({
    'get': 'list'
})
urlpatterns = [
    path('list/', course_view),
    path('enroll/', csrf_exempt(enroll)),
    path('leave/', csrf_exempt(leave))
    # path('enroll/', csrf_exempt(EnrollmentView.as_view()))
]
