from django.urls import include, path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('upload/', views.upload, name="upload"),
	path('search/', views.search, name="search"),
	path('genes/', views.index, name="index"),
	path('gene/<str:gene_name>', views.gene, name="gene"),
	path('variants/', views.variants, name="variants"),
	path('gene/<str:gene_name>/variant/<str:variant_p>', views.variant, name="variant"),
	path('gene/<str:gene_name>/variant/<str:variant_p>/save', views.save, name="save_variant"),
	path('gene/<str:gene_name>/variant/<str:variant_p>/result', views.variant_text, name="variant_text"),
	path('gene/<str:gene_name>/variant/<str:variant_p>/export', views.export, name="export"),
	path('gene/<str:gene_name>/variant/<str:variant_p>/exported', views.exported, name="exported"),
	path('gene/<str:gene_name>/variant/<str:variant_p>/history', views.history, name="history"),
]

