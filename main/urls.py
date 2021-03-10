from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('request/', views.account_request, name='request'),
    path('genes/', views.genes, name='genes'),
    path('gene/', views.gene, name='variants'),
    path('gene/<str:gene_name>', views.gene, name='gene'),
    path('gene/<str:gene_name>/variant/<str:protein>', views.variant, name='variant'),
    path('gene/<str:gene_name>/variant/<str:protein>/detail', views.variant_text, name='variant_text'),
    path('gene/<str:gene_name>/variant/<str:protein>/export', views.export, name='export'),
    path('gene/<str:gene_name>/variant/<str:protein>/exported', views.exported, name='exported'),
    path('gene/<str:gene_name>/variant/<str:protein>/history', views.history, name='history'),
]
