import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
def test_product_serializer_serialization():

    category_list = [CategoryFactory() for _ in range(3)]
    product = ProductFactory()

    product.category.set(category_list)
    serializer = ProductSerializer(product)
    data = serializer.data

    assert data['title'] == product.title
    assert data['description'] == product.description
    assert data['price'] == product.price
    assert data['active'] == product.active
    assert len(data['category']) == len(category_list)
    
    serialized_slugs = data['category']
    factory_slugs = [cat.slug for cat in category_list]
    assert set(serialized_slugs) == set(factory_slugs)


@pytest.mark.django_db
def test_product_serializer_deserialization():    
    category_list = [CategoryFactory() for _ in range(3)]
    category_list_slugs = [cat.slug for cat in category_list]

    input_data = {
        'title': 'Test Product',         
        'description': 'Product description',      
        'price': 87,                          
        'active': True,                         
        'category': category_list_slugs,
    }

    serializer = ProductSerializer(data=input_data)

    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
    product = serializer.save()

    assert product.title == input_data['title']
    assert product.description == input_data['description']
    assert product.price == input_data['price']
    assert product.active == input_data['active']

    product_category_slugs = [cat.slug for cat in product.category.all()]

    assert set(category_list_slugs) == set(product_category_slugs), f"Expected categories: {category_list_slugs}, Found: {product_category_slugs}"