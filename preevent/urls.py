from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Setup the URLs and include login URLs for the browsable API.
router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'seats', views.SeatBookingViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'payment/', views.payment),
]
