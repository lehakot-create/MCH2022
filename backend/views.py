from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Product, Favourite, Profile, ProfileCompany
from .serializers import *
from .filters import CompanyFilter, ProductFilter
from .forms import ManufacturerForm, ProductForm

from .utils import remove_dublicate


class RegionListApiView(generics.ListAPIView):
    """
    Возвращает список регионов
    """
    queryset = Company.objects.values('Region').distinct('Region')
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        region = self.get_queryset()
        serializer = RegionSerializer(region, many=True)
        return Response(serializer.data)


class RegionDetailApiView(APIView):
    """
    Возвращает все записи с заданным регионом
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(Region=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('region'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class LocalityListApiView(generics.ListAPIView):
    """
    Возвращает список всех городов
    """
    queryset = Company.objects.values('Locality').distinct('Locality')
    serializer_class = LocalitySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        locality = self.get_queryset()
        serializer = LocalitySerializer(locality, many=True)
        return Response(serializer.data)


class LocalityDetailApiView(APIView):
    """
    Возвращает все записи с заданным городом
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(Locality=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('locality'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class InnDetailApiView(APIView):
    """
    Возвращает компанию по ее ИНН
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(INN=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('inn'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CategoriesListApiView(generics.ListAPIView):
    """
    Возвращает список категорий
    """
    queryset = Company.objects.values('Categories').distinct('Categories')
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        categories_raw = self.get_queryset()
        categories = self.remove_dublicate(key='Categories', data=categories_raw)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def remove_dublicate(self, key, data):
        """
        Убирает дубликаты из queryset
        :param queryset: получает queryset
        :return: {'categories': [cat1, cat2, cat3, ... cat_n]}
        """
        lst = []
        for dct in data:
            if dct.get(key) is not None:
                for el in dct.get(key):
                    if el not in lst:
                        lst.append(el)
        lst_out = list(map(lambda x: {key: x}, lst))
        return lst_out


class CategoriesDetailApiView(APIView):
    """
    Возвращает компании по заданной категории
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(Categories__icontains=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('category'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class ProductListApiView(generics.ListAPIView):
    """
    Возвращает список всех продуктов
    """
    queryset = Company.objects.values('Products').distinct('Products')
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        products_raw = self.get_queryset()
        products = self.remove_dublicate(key='Products', data=products_raw)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    def remove_dublicate(self, key, data):
        """
        Убирает дубликаты из queryset
        :param queryset: получает queryset
        :return: {'categories': [cat1, cat2, cat3, ... cat_n]}
        """
        lst = []
        for dct in data:
            if dct.get(key) is not None:
                for el in dct.get(key):
                    if el not in lst:
                        lst.append(el)
        lst_out = list(map(lambda x: {key: x}, lst))
        return lst_out


class ProductDetailApiView(APIView):
    """
    Возвращает все записи с заданным продуктом
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(Products__icontains=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('product'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class ApiIdDetailApiView(APIView):
    """
    Возвращает запись по id
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Company.objects.filter(id=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        companies = self.get_object(kwargs.get('id'))
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class FavouriteListApiView(generics.ListAPIView):
    """
    Возвращает все избранные компании данного юзера
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer

    def get_queryset(self, request):
        try:
            return Favourite.objects.filter(user=request.user.id)
        except Favourite.DoesNotExist:
            raise Http404

    def list(self, request):
        favourite_company = self.get_queryset(self.request)
        data = []
        for el in favourite_company.values('company'):
            company = Company.objects.get(id=el.get('company'))
            data.append({
                'id': el.get('company'),
                'name': company.Company
            })
        serializer = NewNewFavouriteSerializer(data, many=True)
        return Response(serializer.data)


class FavouriteDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None, **kwargs):
        """
        Добавляет компанию в избранное юзера
        """
        company = Company.objects.get(id=kwargs.get('pk'))
        user = User.objects.get(id=request.user.id)
        if not Favourite.objects.filter(user=user, company=company).exists():
            try:
                Favourite.objects.create(user=User.objects.get(id=request.user.id), company=company)
                return Response({'id': company.id, 'name': company.Company})
            except Company.DoesNotExist:
                return JsonResponse({'error': 'Компания не найдена'})
        return JsonResponse({'error': 'Запись уже существует'})

    def delete(self, request, **kwargs):
        """
        Удаляет компанию из избранных юзера
        """
        try:
            favourite_company = Favourite.objects.get(user=User.objects.get(id=request.user.id),
                                                      company=kwargs.get('pk'))
            favourite_company.delete()
            return JsonResponse({'detail': 'Компания удалена из избранных'})
        except Favourite.DoesNotExist:
            return JsonResponse({'error': 'Компания не найдена'})


class FindApiList(APIView):
    """
    Обеспечивает поиск по множеству условий
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get(self, request):
        data = request.GET
        try:
            last = Profile.objects.get(user=request.user.id)
            last.last_request = data
            last.save()

            find = data.get('find')
            if find.isdigit() and len(find) == 10:
                company = Company.objects.filter(INN=find)
            else:
                company = Company.objects.filter(
                    Q(Company__icontains=find) |
                    Q(Direction__icontains=find) |
                    Q(Description__icontains=find) |
                    Q(Categories__icontains=find) |
                    Q(Products__icontains=find) |
                    Q(Region__icontains=find) |
                    Q(Locality__icontains=find) |
                    Q(Address__icontains=find)
                )
            serializer = CompanySerializer(company, many=True)
            return Response(serializer.data)
        except Company.DoesNotExist or Profile.DoesNotExist:
            raise Http404


class LastApiList(APIView):
    """
    Возвращает последний запрос пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get(self, request):
        try:
            last = Profile.objects.get(user=request.user.id)
            data = last.last_request

            company = Company.objects.filter(
                Q(Company=data.get('company', None)) |
                Q(Categories=data.get('categories', None)) |
                Q(Products=data.get('products', None)) |
                Q(INN=data.get('inn', None)) |
                Q(Region=data.get('region', None)) |
                Q(Locality=data.get('locality', None)) |
                Q(Address=data.get('address', None))
            )
            serializer = CompanySerializer(company, many=True)
            return Response(serializer.data)
        except Company.DoesNotExist or Profile.DoesNotExist:
            raise Http404
        except AttributeError:
            return Response({'error': 'Последних запросов нет'}, status=status.HTTP_400_BAD_REQUEST)


class QuantityApiList(APIView):
    """
    Возвращает количество компаний и продуктов в БД
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            qty_company = Company.objects.all().count()
            qty_product_raw = Company.objects.values('Products').distinct('Products')
            qty_product = len(self.remove_dublicate(key='Products', data=qty_product_raw))
            return Response({'qty_company': qty_company,
                             'qty_product': qty_product})
        except Company.DoesNotExist:
            raise Http404

    def remove_dublicate(self, key, data):
        """
        Убирает дубликаты из queryset
        :param queryset: получает queryset
        :return: {'categories': [cat1, cat2, cat3, ... cat_n]}
        """
        lst = []
        for dct in data:
            if dct.get(key) is not None:
                for el in dct.get(key):
                    if el not in lst:
                        lst.append(el)
        lst_out = list(map(lambda x: {key: x}, lst))
        return lst_out
