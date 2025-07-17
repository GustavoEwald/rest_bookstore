from rest_framework import serializers

from order.models.order import Order
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    product_deserial = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='title',
        many=True,
        required=True,
        write_only=True
    )

    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum(product.price for product in instance.product.all())
        return total

    class Meta:
        model = Order
        fields = ['product', 'product_deserial', 'user', 'total']

    def create(self, validated_data):
        product_data = validated_data.pop('product_deserial')
        order = Order.objects.create(**validated_data)

        for product_title in product_data:
            product_instance = Product.objects.get(title=product_title)
            order.product.add(product_instance)

        return order