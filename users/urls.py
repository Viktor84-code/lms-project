from django.urls import path

from .views import UserProfileUpdateView, PaymentListView

urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="profile-update"),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]
