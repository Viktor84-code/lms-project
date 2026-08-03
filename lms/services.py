import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from users.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name, description):
    return stripe.Product.create(
        name=name,
        description=description,
        tax_code='txcd_10103001',
    )


def create_price(product_id, amount, currency='rub'):
    return stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency=currency,
    )


def create_checkout_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        line_items=[{'price': price_id, 'quantity': 1}],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        managed_payments={'enabled': True},
    )


def retrieve_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)


class CoursePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        try:
            product = create_product(course.title, course.description)
            price = create_price(product.id, course.price)
            session = create_checkout_session(
                price_id=price.id,
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )

            Payment.objects.create(
                user=user,
                course=course,
                amount=course.price,
                payment_method='transfer',
                stripe_session_id=session.id,
                stripe_payment_url=session.url,
            )

            return Response({
                'payment_url': session.url,
                'session_id': session.id,
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)
