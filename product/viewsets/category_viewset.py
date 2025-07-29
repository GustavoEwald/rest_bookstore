from rest_framework import viewsets

from product.models import Category
from product.serializers.category_serializer import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()
