from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view()
def view_products(request):
    return Response({'message':'okay'})

@api_view()
def view_categories(request):
    return Response({'message':'okay'})