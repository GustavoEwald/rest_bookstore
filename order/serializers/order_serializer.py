from rest_framework import serializers

from order.models.order import Order
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer
from django.contrib.auth.models import User

class OrderSerializer(serializers.ModelSerializer):
    #product = ProductSerializer(many=True, required=True)
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='title', many=True)
    total = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total
    class Meta:
        model = Order
        fields = ['product', 'total', 'user']