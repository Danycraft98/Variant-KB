from rest_framework import viewsets, generics



from .serializers import *
from .models import Gene, Variant


class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all().order_by('name')
    serializer_class = GeneSerializer


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class DiseaseViewSet(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class DiseaseList(viewsets.ViewSetMixin, generics.ListAPIView):
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        queryset = Disease.objects.all()
        name = self.kwargs.get('name', None)
        if name:
            queryset = queryset.filter(name=name)
        return queryset

    @classmethod
    def get_extra_actions(cls):
        return []
