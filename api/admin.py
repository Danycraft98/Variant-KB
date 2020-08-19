from django.contrib import admin

# Register your models here.
from .models import Variant, Gene, Evidence


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 3


class GeneAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'content']}),
                 ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [VariantInline]


# admin.site.register(Gene)
# admin.site.register(Variant)
admin.site.register(Gene, GeneAdmin)
admin.site.register(Variant)
admin.site.register(Evidence)
