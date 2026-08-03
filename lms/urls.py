from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lms.services import CoursePaymentView
from lms.views import SubscriptionView, PaymentStatusView
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyView.as_view(), name="lesson-detail"),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('courses/<int:course_id>/pay/', CoursePaymentView.as_view(), name='course-pay'),
    path('payment/<str:session_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
]
