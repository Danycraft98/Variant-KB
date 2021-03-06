from rest_framework import serializers

from .models import Disease, Variant, Gene


class DiseaseSerializer(serializers.ModelSerializer):
    gene = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()
    gdr = serializers.SerializerMethodField()

    @staticmethod
    def get_gene(obj):
        return obj.variant.gene.id

    @staticmethod
    def get_variant(obj):
        return obj.variant.id

    @staticmethod
    def get_gdr(obj):
        report = obj.reports.filter(name='Gene-Disease').first()
        if report:
            return report.content
        return ''

    class Meta:
        model = Disease
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    diseases = DiseaseSerializer(required=False, many=True)

    class Meta:
        model = Variant
        fields = '__all__'


class GeneSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(required=False, many=True)

    class Meta:
        model = Gene
        fields = ('name', 'content', 'variants')
