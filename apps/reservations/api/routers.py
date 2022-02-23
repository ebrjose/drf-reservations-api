from rest_framework.routers import DefaultRouter
from apps.reservations.api.api import ReservationViewSet

router = DefaultRouter()
router.register('', ReservationViewSet, basename="reservations")

urlpatterns = router.urls