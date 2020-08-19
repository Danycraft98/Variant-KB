from rest_framework import serializers

from .models import Variant, Gene


class VariantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Variant
        fields = ('name', 'g_dna', 'protein')


class GeneSerializer(serializers.HyperlinkedModelSerializer):
    variants = VariantSerializer(required=False, many=True)

    class Meta:
        model = Gene
        fields = ('name', 'content', 'variants')
