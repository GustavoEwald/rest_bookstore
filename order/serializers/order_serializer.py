from rest_framework import serializers

from order.models.order import Order
from product.serializers.product_serializer import ProductSerializer
from product.models import Product

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, required=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total
    class Meta:
        model = Order
        fields = ['product', 'total']