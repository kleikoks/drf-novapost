from django.urls import path, include
from .views import SettlementsViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'settlements', SettlementsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
