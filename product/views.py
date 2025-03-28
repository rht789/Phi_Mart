from django.shortcuts import render, get_object_or_404
from product.models import Product,Category
from product.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view()
def view_specific_products(request,id):
    product=get_object_or_404(Product, pk=id)
    serializer=ProductSerializer(product)
    print(serializer.data)
    return Response(serializer.data)

@api_view()
def view_categories(request):
    return Response({'message':'okay'})