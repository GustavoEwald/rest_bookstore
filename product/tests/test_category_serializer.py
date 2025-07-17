import pytest

from product.factories import CategoryFactory
from product.serializers.category_serializer import CategorySerializer
from product.models import Category

@pytest.mark.django_db
def test_category_serializer_serialization():
    category = CategoryFactory()
    serializer = CategorySerializer(category)
    data = serializer.data

    assert data['title'] == category.title
    assert data['slug'] == category.slug
    assert data['description'] == category.description
    assert data['active'] == category.active

@pytest.mark.django_db
def test_category_serializer_deserialization():
    
    data = {
        "title": "New Category",
        "slug": "new-category",
        "description": "A new category for testing.",
        "active": True
    }

    serializer = CategorySerializer(data=data)
    assert serializer.is_valid()

    category = serializer.save()
    assert category.title == data['title']
    assert category.slug == data['slug']
    assert category.description == data['description']
    assert category.active == data['active']
    assert Category.objects.count() == 1