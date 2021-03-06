from rest_framework import viewsets

from apps.rooms.api.serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset =  RoomSerializer.Meta.model.objects.filter(active=True)


    # def get_queryset(self, pk=None):
    #     if pk is None:
    #         return self.get_serializer().Meta.model.objects.filter(active=True)
    #     return self.get_serializer().Meta.model.objects.filter(id=pk, active=True).first()
