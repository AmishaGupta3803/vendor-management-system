from django.shortcuts import render
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer, AcknowledgePurchaseOrderSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Create your views here.

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    serializer_class = VendorPerformanceSerializer

    def get_object(self):
        vendor_id = self.kwargs.get('vendor_id')
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        return vendor

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    serializer_class = AcknowledgePurchaseOrderSerializer

    def get_object(self):
        po_id = self.kwargs.get('po_id')
        return get_object_or_404(PurchaseOrder, pk=po_id)

    def perform_update(self, serializer):
        acknowledgment_date = serializer.validated_data.get('acknowledgment_date')
        if acknowledgment_date is not None:
            serializer.instance.acknowledgment_date = acknowledgment_date
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
