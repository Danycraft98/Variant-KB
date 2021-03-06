from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'genes', views.GeneViewSet)
router.register(r'variants', views.VariantViewSet)
router.register(r'diseases', views.DiseaseViewSet)
router.register(r'disease/(?P<name>.+)', views.DiseaseList, basename='disease')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include((router.urls, 'variant_db'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
