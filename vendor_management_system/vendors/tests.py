from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Vendor, PurchaseOrder

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test St, Test City',
            'vendor_code': 'TEST001'
        }
        self.response = self.client.post(
            reverse('vendor-list-create'),
            self.vendor_data,
            format='json'
        )

    def get_access_token(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        return response.data['access']

    def test_vendor_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_vendor_list(self):
        response = self.client.get(reverse('vendor-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.vendor_data['name'])
        self.assertContains(response, self.vendor_data['contact_details'])
        self.assertContains(response, self.vendor_data['address'])
        self.assertContains(response, self.vendor_data['vendor_code'])

    def test_vendor_retrieve(self):
        vendor = Vendor.objects.first()
        response = self.client.get(reverse('vendor-retrieve-update-destroy', kwargs={'pk': vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])
        self.assertEqual(response.data['contact_details'], self.vendor_data['contact_details'])
        self.assertEqual(response.data['address'], self.vendor_data['address'])
        self.assertEqual(response.data['vendor_code'], self.vendor_data['vendor_code'])

    def test_vendor_update(self):
        vendor = Vendor.objects.first()
        update_data = {
            'name': 'Updated Vendor Name',
            'contact_details': 'updated_test@example.com',
            'address': '456 Updated St, Updated City',
            'vendor_code': 'UPDATED001'
        }
        response = self.client.put(
            reverse('vendor-retrieve-update-destroy', kwargs={'pk': vendor.id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])
        self.assertEqual(response.data['contact_details'], update_data['contact_details'])
        self.assertEqual(response.data['address'], update_data['address'])
        self.assertEqual(response.data['vendor_code'], update_data['vendor_code'])

    def test_vendor_delete(self):
        vendor = Vendor.objects.first()
        response = self.client.delete(reverse('vendor-retrieve-update-destroy', kwargs={'pk': vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class PurchaseOrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='123 Test St, Test City',
            vendor_code='TEST001'
        )
        self.po_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': '2024-05-05T12:00:00Z',
            'delivery_date': '2024-05-10T12:00:00Z',
            'items': ['Item 1', 'Item 2'],
            'quantity': 10,
            'status': 'pending'
        }
        self.response = self.client.post(
            reverse('purchase-order-list-create'),
            self.po_data,
            format='json'
        )

    def get_access_token(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpassword'},
            format='json'
        )
        return response.data['access']

    def test_purchase_order_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_purchase_order_list(self):
        response = self.client.get(reverse('purchase-order-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.po_data['po_number'])
        self.assertContains(response, self.po_data['order_date'])
        self.assertContains(response, self.po_data['delivery_date'])
        self.assertContains(response, self.po_data['status'])

    def test_purchase_order_retrieve(self):
        purchase_order = PurchaseOrder.objects.first()
        response = self.client.get(reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': purchase_order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.po_data['po_number'])
        self.assertEqual(response.data['order_date'], self.po_data['order_date'])
        self.assertEqual(response.data['delivery_date'], self.po_data['delivery_date'])
        self.assertEqual(response.data['status'], self.po_data['status'])

    def test_purchase_order_update(self):
        purchase_order = PurchaseOrder.objects.first()
        update_data = {
            'po_number': 'PO002',
            'vendor': self.vendor.id,
            'order_date': '2024-05-06T12:00:00Z',
            'delivery_date': '2024-05-11T12:00:00Z',
            'items': ['Item 3', 'Item 4'],
            'quantity': 20,
            'status': 'completed'
        }
        response = self.client.put(
            reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': purchase_order.id}),
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], update_data['po_number'])
        self.assertEqual(response.data['order_date'], update_data['order_date'])
        self.assertEqual(response.data['delivery_date'], update_data['delivery_date'])
        self.assertEqual(response.data['status'], update_data['status'])

    def test_purchase_order_delete(self):
        purchase_order = PurchaseOrder.objects.first()
        response = self.client.delete(reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': purchase_order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
