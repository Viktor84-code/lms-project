from django.urls import path

from .views import PaymentListView, UserProfileUpdateView

urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="profile-update"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
]
