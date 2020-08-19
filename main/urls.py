from django.urls import include, path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('upload/', views.upload, name="upload"),
	path('search/', views.search, name="search"),
	path('genes/', views.index, name="index"),
	path('gene/<int:gene_id>', views.gene, name="gene"),
	path('variants/', views.variants, name="variants"),
	path('variant/<int:variant_id>', views.variant, name="variant"),
	path('variant/<int:variant_id>/save', views.save, name="save_variant"),
	path('variant/<int:variant_id>/result', views.variant_text, name="variant_text"),
	path('variant/<int:variant_id>/export', views.export, name="export"),
	path('variant/<int:variant_id>/exported', views.exported, name="exported"),
	path('variant/<int:variant_id>/history', views.history, name="history"),
]

