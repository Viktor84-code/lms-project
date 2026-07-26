from django.urls import path

from users.views import (
    UserRegistrationView, UserListView, UserDetailView
)
from .views import PaymentListView, UserProfileUpdateView

urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="profile-update"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path('profile/<int:pk>/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),

    # Новые маршруты:
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
