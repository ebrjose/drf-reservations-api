from rest_framework.routers import DefaultRouter
from apps.rooms.api.api import RoomViewSet

router = DefaultRouter()
router.register('', RoomViewSet, basename='rooms')

urlpatterns = router.urls