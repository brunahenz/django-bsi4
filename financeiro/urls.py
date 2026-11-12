from rest_framework.routers import DefaultRouter
from .views import (
    ContaViewSet,
    CategoriaViewSet,
    LancamentoViewSet,
    OrcamentoViewSet
)

router = DefaultRouter()

router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('lancamentos', LancamentoViewSet, basename='lancamento')
router.register('orcamentos', OrcamentoViewSet, basename='orcamento')

urlpatterns = router.urls 
