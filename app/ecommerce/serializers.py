from rest_framework import serializers
from core.models import(
    Customer,
    Flower,
    Order,
    orderItem
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user'] 
    
    def create(self, validated_data):
        request = self.context.get('request')
        auth_user = request.user
        
        # Add user to validated_data before creating customer
        validated_data['user'] = auth_user
        customer = Customer.objects.create(**validated_data)
        
        return customer
    
class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flower
        fields="__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderItem
        fields = ['id', 'flower', 'quantity', 'price']
        read_only_fields = ['price']

    def create(self, validated_data):
        flower = validated_data.get('flower')
        validated_data['price'] = flower.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'items']
        read_only_fields = ['customer', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        
        request = self.context.get('request')
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.create(customer=customer, **validated_data)

        for item_data in items_data:
            orderItem.objects.create(order=order, **item_data)

        return order
