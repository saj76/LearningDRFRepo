from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from registers.views import ShopsListView
from registers.views import GetRegistersCountByDateViewSet

router = DefaultRouter()
router.register(r'shops', ShopsListView, "list")
router.register(r'get_registers_count_by_date', GetRegistersCountByDateViewSet, 'get_registers_count_by_date')

urlpatterns = [
    path('shops/', include(router.urls)),
]