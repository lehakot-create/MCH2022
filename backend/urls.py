from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('moderate/companies', CompaniesAdminViewSet, basename='moderate-companies')
router.register('moderate/companies/<int:pk>', CompaniesAdminViewSet, basename='moderate-company')
router.register('companies', CompaniesUserViewSet, basename='companies')
router.register('profile/companies', CompaniesManufacturerViewSet, basename='manufacturer-companies')
# router.register('moderate/set_parser', set_parser_days)

urlpatterns = [
    path('api/v1/regions/', RegionListApiView.as_view()),
    path('api/v1/region/<str:region>/', RegionDetailApiView.as_view()),

    path('api/v1/locality/', LocalityListApiView.as_view()),
    path('api/v1/locality/<str:locality>/', LocalityDetailApiView.as_view()),

    path('api/v1/inn/<int:inn>/', InnDetailApiView.as_view()),

    path('api/v1/categories/', CategoriesListApiView.as_view()),
    path('api/v1/category/<str:category>/', CategoriesDetailApiView.as_view()),

    path('api/v1/products/', ProductListApiView.as_view()),
    path('api/v1/product/<str:product>/', ProductDetailApiView.as_view()),

    path('api/v1/api_id/<int:id>/', ApiIdDetailApiView.as_view()),

    path('api/v1/favourite/', FavouriteDetailApiView.as_view()),

    path('api/v1/find/', FindApiList.as_view()),
    path('api/v1/last/', LastApiList.as_view()),

    path('api/v1/quantity/', QuantityApiList.as_view()),
    path('api/v1/analitics/categories/', AnaliticsQuantityCompanyApiView.as_view()),
    path('api/v1/analitics/directions/', AnaliticsQuantityDirectionApiView.as_view()),
    path('api/v1/analitics/locality/', AnaliticsQuantityLocalityApiView.as_view()),

    path('api/v1/', include(router.urls)),
]
