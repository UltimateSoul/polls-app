"""Api app urls module"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import PollViewSet

router = routers.DefaultRouter()
router.register(r'polls', PollViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
