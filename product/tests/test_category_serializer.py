import pytest

from product.factories import CategoryFactory
from product.serializers.category_serializer import CategorySerializer
from product.models import Category

@pytest.mark.django_db
def test_category_serializer_output():
    category = CategoryFactory()
    serializer = CategorySerializer(category)
    data = serializer.data

    assert data['title'] == category.title
    assert data['slug'] == category.slug
    assert data['description'] == category.description
    assert data['active'] == category.active

@pytest.mark.django_db
def test_category_serializer_deserialization():
    # Test data mimicking what would come from a client (e.g., in a POST request)
    data = {
        "title": "New Category",
        "slug": "new-category",
        "description": "A new category for testing.",
        "active": True
    }

    # Create the serializer with data and check if it's valid
    serializer = CategorySerializer(data=data)
    
    # Check that the data is valid
    assert serializer.is_valid()

    # Save the data into the database (this creates a Category instance)
    category = serializer.save()

    # Ensure the Category object has been created with the correct data
    assert category.title == data['title']
    assert category.slug == data['slug']
    assert category.description == data['description']
    assert category.active == data['active']
    
    # Optionally, check that the object was actually created in the database
    assert Category.objects.count() == 1  # Ensure one category is saved