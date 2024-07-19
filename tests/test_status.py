from django.test import TestCase
from django.conf import settings
from django.db.models.signals import post_save
from django.test.utils import override_settings
from order_and_shop.models import Order, Shop
from order_and_shop.signals import order_status_changed
from unittest.mock import patch
import requests_mock

# Отключаем сигналы для других тестов
@override_settings(API_KEY='test_api_key')
class OrderAndShopTests(TestCase):
    def setUp(self):
        # Подключаем сигнал вручную для тестов
        post_save.connect(order_status_changed, sender=Order)

    def tearDown(self):
        # Отключаем сигнал после тестов
        post_save.disconnect(order_status_changed, sender=Order)

    @requests_mock.Mocker()
    def test_order_status_change_triggers_api_call(self, mock_request):
        # Мокаем внешний API
        mock_request.post('https://example.com/api/send_order', json={'success': True}, status_code=200)

        # Создаем тестовый магазин и заказ
        shop = Shop.objects.create(name='Test Shop', status='open')
        order = Order.objects.create(shop=shop, status='complete', order_id='order1')

        # Проверяем, что запрос был отправлен
        self.assertTrue(mock_request.called)
        self.assertEqual(mock_request.call_count, 1)

        # Проверяем параметры запроса
        request = mock_request.request_history[0]
        self.assertEqual(request.json(), {'orderid': order.order_id, 'shpid': shop.id})
        self.assertEqual(request.headers['Authorization'], f'Bearer {settings.API_KEY}')

    @requests_mock.Mocker()
    def test_order_status_change_with_unstable_connection(self, mock_request):
        # Мокаем нестабильное соединение
        mock_request.post('https://example.com/api/send_order', exc=requests.RequestException)

        # Создаем тестовый магазин и заказ
        shop = Shop.objects.create(name='Test Shop', status='open')
        order = Order.objects.create(shop=shop, status='complete', order_id='order1')

        # Проверяем количество попыток
        self.assertEqual(mock_request.call_count, 3)

    def test_order_status_change_does_not_trigger_api_call_when_shop_closed(self):
        with patch('order_and_shop.utils.send_order_to_external_api') as mock_send_order:
            # Создаем тестовый магазин и заказ
            shop = Shop.objects.create(name='Test Shop', status='closed')
            Order.objects.create(shop=shop, status='complete', order_id='order1')

            # Проверяем, что запрос не был отправлен
            mock_send_order.assert_not_called()

    def test_order_status_change_does_not_trigger_api_call_when_order_not_complete(self):
        with patch('order_and_shop.utils.send_order_to_external_api') as mock_send_order:
            # Создаем тестовый магазин и заказ
            shop = Shop.objects.create(name='Test Shop', status='open')
            Order.objects.create(shop=shop, status='pending', order_id='order1')

            # Проверяем, что запрос не был отправлен
            mock_send_order.assert_not_called()
