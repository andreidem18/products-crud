from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from config.get_client_ip import get_client_ip
from .models import Product
from rest_framework import serializers, viewsets



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'isAvailable')
        
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product = Product.objects.create(
            name=request.data['name'],
            category=request.data['category'],
            price=request.data['price'],
            isAvailable=request.data['isAvailable'],
            created_by=get_client_ip(request)
        )
        serialized = ProductSerializer(product)
        return Response(status = status.HTTP_201_CREATED, data = serialized.data)
