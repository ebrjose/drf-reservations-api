from django.shortcuts import get_object_or_404

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.reservations.models import Reservation
from apps.reservations.api.serializers import (
    ReservationSerializer,
    ReservationListSerializer,
    ReservationViewSerializer,
    ReservationStatusSerializer
)

class ReservationViewSet(viewsets.GenericViewSet):
    model = Reservation
    serializer_class = ReservationSerializer
    list_serializer_class = ReservationListSerializer
    view_serializer_class = ReservationViewSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(active=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, active=True).first()

    def list(self, request):
        reservations = self.get_queryset()
        reservation_serializer = self.list_serializer_class(reservations, many=True)
        return Response(reservation_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        reservation = self.get_object(pk)
        reservation_serializer = self.view_serializer_class(reservation)
        return Response(reservation_serializer.data)

    @action(detail=False, methods=['post'], url_path='make')
    def book(self, request):
        reservation_serializer = self.serializer_class(data=request.data)
        if reservation_serializer.is_valid():
            reservation_serializer.save()

            return Response(reservation_serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'errors': reservation_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, pk=None):
        reservation = self.get_object(pk)
        reservation.status = 'CANCELLED'
        reservation.save()

        reservation_serializer = ReservationStatusSerializer(reservation)
        return Response(reservation_serializer.data, status=status.HTTP_200_OK)
