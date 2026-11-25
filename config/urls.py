from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from financeiro.views import dashboard, pagina_contas, pagina_categorias, pagina_lancamentos, pagina_orcamentos



router = DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/financeiro/", include("financeiro.urls")),
    path("", dashboard, name="dashboard"),
    path("contas/", pagina_contas, name="pagina_contas"),
    path("categorias/", pagina_categorias, name="pagina_categorias"),
    path("lancamentos/", pagina_lancamentos, name="pagina_lancamentos"),
    path("orcamentos/", pagina_orcamentos, name="pagina_orcamentos"),

]


