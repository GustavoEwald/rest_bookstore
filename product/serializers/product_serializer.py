from rest_framework import serializers

from product.serializers.category_serializer import CategorySerializer
from product.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    #category = CategorySerializer(many=True, required=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug', many=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'active', 'category']