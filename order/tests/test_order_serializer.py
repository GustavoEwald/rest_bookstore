import pytest

from django.contrib.auth.models import User
from order.factories import OrderFactory
from order.serializers.order_serializer import OrderSerializer
from product.factories import CategoryFactory, ProductFactory

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
    assert data['product'][0]['price'] == product_1.price
    assert data['product'][1]['price'] == product_2.price