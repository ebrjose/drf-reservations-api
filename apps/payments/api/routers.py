from rest_framework.routers import DefaultRouter
from apps.payments.api.api import PaymentsViewSet

router = DefaultRouter()
router.register('', PaymentsViewSet, basename='payments')

urlpatterns = router.urls