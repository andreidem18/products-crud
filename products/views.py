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
        
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'isAvailable', 'created_by')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(created_by=get_client_ip(request))
        serialized = ProductSerializer(queryset, many=True)
        return Response(serialized.data)

    def create(self, request, *args, **kwargs):
        request.data['created_by']=get_client_ip(request)
        serialized = CreateProductSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serialized.errors)
        else:
            serialized.save()
            serialized = ProductSerializer(serialized.data)
            return Response(status = status.HTTP_201_CREATED, data = serialized.data)
            