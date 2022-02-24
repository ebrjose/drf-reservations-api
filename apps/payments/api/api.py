from django.shortcuts import get_object_or_404

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.reservations.models import Reservation
from apps.payments.models import Payment

from apps.payments.api.serializers import (
    ProcessPaymentSerializer,
    ViewPaymentSerializer,
    PaymentListSerializer
)

class PaymentsViewSet(viewsets.GenericViewSet):
    model = Payment
    serializer_class = PaymentListSerializer
    list_serializer_class = PaymentListSerializer
    view_serializer_class = ViewPaymentSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(active=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=True).first()

    def list(self, request):
        payments = self.get_queryset()
        list_serializer = self.list_serializer_class(payments, many=True)
        return Response(list_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        payment = self.get_object(pk)
        view_serializer = self.view_serializer_class(payment)
        return Response(view_serializer.data)

    @action(detail=False, methods=['post'], url_path='process')
    def process_payment(self, request):
        process_serializer = ProcessPaymentSerializer(data=request.data)

        if process_serializer.is_valid():
            process_serializer.save()
            view_serializer = self.view_serializer_class(
                self.get_object(pk=process_serializer.data['id'])
            )
            return Response(view_serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'errors': process_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)