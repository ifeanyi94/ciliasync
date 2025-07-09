from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalysisResultViewSet, filtered_results

router = DefaultRouter()
router.register(r'results', AnalysisResultViewSet)

urlpatterns = [
    path('results/filter/', filtered_results),  # ✅ Place BEFORE router
    path('', include(router.urls)),
]
