from django.shortcuts import render, get_object_or_404
from product.models import Product,Category
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view()
def view_specific_products(request,id):
    product=get_object_or_404(Product, pk=id)
    product_dict={"id":product.id, "name":product.name, "price":product.price}
    return Response(product_dict)

@api_view()
def view_categories(request):
    return Response({'message':'okay'})