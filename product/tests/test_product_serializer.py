import pytest

from product.factories import CategoryFactory, ProductFactory
from product.serializers.product_serializer import ProductSerializer
from product.models import Category

@pytest.mark.django_db
def test_product_serializer_output():

    category_list = [CategoryFactory() for _ in range(3)]
    product = ProductFactory()

    product.category.set(category_list)
    serializer = ProductSerializer(product)
    data = serializer.data

    assert data['title'] == product.title
    assert data['description'] == product.description
    assert data['price'] == product.price
    assert data['active'] == product.active

    assert len(data['category']) == len(category_list)  # Check categories count
    serialized_slugs = data['category']
    factory_slugs = [cat.slug for cat in category_list]  # Get slugs from factory-created categories

    assert set(serialized_slugs) == set(factory_slugs)  # Ensure the slugs match


@pytest.mark.django_db
def test_product_serializer_deserialization():
    # Step 1: Manually create Category instances
    category1 = Category.objects.create(title="Category 1", slug="category-1", description="Description 1", active=True)
    category2 = Category.objects.create(title="Category 2", slug="category-2", description="Description 2", active=True)
    category3 = Category.objects.create(title="Category 3", slug="category-3", description="Description 3", active=True)

    # Step 2: Prepare the input data for the Product serializer
    input_data = {
        'title': 'Test Product',                # Product title
        'description': 'A sample product',      # Product description
        'price': 1999,                          # Product price
        'active': True,                         # Product is active
        'category': [                           # Categories (pass slugs of existing categories)
            category1.slug,
            category2.slug,
            category3.slug,
        ],
    }

    # Step 3: Create the serializer instance with the input data
    serializer = ProductSerializer(data=input_data)

    # Step 4: Check if the serializer is valid
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"

    # Step 5: Save the product instance after deserialization
    product = serializer.save()

    # Step 6: Check that the product fields were correctly populated
    assert product.title == input_data['title']
    assert product.description == input_data['description']
    assert product.price == input_data['price']
    assert product.active == input_data['active']

    category_slugs = [category1.slug, category2.slug, category3.slug]
    product_category_slugs = [cat.slug for cat in product.category.all()]


    assert set(category_slugs) == set(product_category_slugs), f"Expected categories: {category_slugs}, Found: {product_category_slugs}"