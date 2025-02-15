from django.shortcuts import render
from rest_framework import viewsets
from core import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ecommerce import serializers

class CustomerViewset(viewsets.ModelViewSet):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]


class FlowerViewSet(viewsets.ModelViewSet):
    queryset=models.Flower.objects.all()
    serializer_class=serializers.FlowerSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return orders for the authenticated user only"""
        customer = models.Customer.objects.get(user=self.request.user)
        return models.Order.objects.filter(customer=customer)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return order items for the authenticated user's orders only"""
        customer = models.Customer.objects.get(user=self.request.user)
        return models.orderItem.objects.filter(order__customer=customer)

# class OrderViewset(viewsets.ModelViewSet):
#     queryset=models.Order.objects.all()
#     serializer_class=serializers.OrderSerializer
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsAuthenticated]
    ###