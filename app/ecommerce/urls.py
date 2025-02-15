from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ecommerce import views


app_name='ecommerce'
router=DefaultRouter()

router.register('customers',views.CustomerViewset)
router.register('flowers',views.FlowerViewSet)
router.register('orders', views.OrderViewSet, basename='order')
router.register('order-items', views.OrderItemViewSet, basename='order-item')

urlpatterns=[
    path('',include(router.urls))
]