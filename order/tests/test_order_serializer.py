import pytest

from django.contrib.auth.models import User
from order.factories import OrderFactory, UserFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import CategoryFactory, ProductFactory
from product.models.category import Category

@pytest.mark.django_db
def test_order_serializer_output():
    product_1 = ProductFactory(price=73)
    product_2 = ProductFactory(price=23)
    product_list = [product_1, product_2]
    
    order = OrderFactory(product=product_list)
    serializer = OrderSerializer(order)

    data = serializer.data

    assert data['total'] == sum([product.price for product in product_list])
    assert len(data['product']) == len(product_list)
    #assert data['product'][0]['price'] == product_1.price
    #assert data['product'][1]['price'] == product_2.price
    assert data['product'][0] == product_1.title
    assert data['product'][1] == product_2.title

@pytest.mark.django_db
def test_order_deserializer_output():
    user = UserFactory()
    category1 = CategoryFactory()
    category2 = CategoryFactory()

    product1 = ProductFactory(title="first product", price=50, category=[category1])
    product2 = ProductFactory(title="second product", price=100, category=[category1, category2])

    data = {
        "product": [
            product1.title,
            product2.title
        ],
        "user": user.id
    }

    serializer = OrderSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    order = serializer.save()
    assert order is not None