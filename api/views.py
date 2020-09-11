from django.shortcuts import render
from rest_framework import viewsets


from .serializers import *
from .models import Gene, Variant


class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all().order_by('name')
    serializer_class = GeneSerializer


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
