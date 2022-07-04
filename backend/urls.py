from django.urls import path
from .views import *


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

    path('api/v1/favourite/', FavouriteListApiView.as_view()),
    path('api/v1/favourite/<int:pk>/', FavouriteDetailApiView.as_view()),

    path('api/v1/find/', FindApiList.as_view()),
    path('api/v1/last/', LastApiList.as_view()),

    path('api/v1/quantity/', QuantityApiList.as_view()),
    path('api/v1/analitics/categories/', AnaliticsQuantityCompanyApiView.as_view()),
    path('api/v1/analitics/directions/', AnaliticsQuantityDirectionApiView.as_view()),
    path('api/v1/analitics/locality/', AnaliticsQuantityLocalityApiView.as_view()),
]
