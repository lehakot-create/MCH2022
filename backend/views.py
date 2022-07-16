from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q, Count
from django.http import Http404, JsonResponse

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Product, Favourite, Profile
from .serializers import *


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
    # permission_classes = [IsAuthenticated]

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


# class FavouriteListApiView(generics.ListAPIView):
#     """
#     Возвращает все избранные компании данного юзера
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = FavouriteSerializer
#
#     def get_queryset(self, request):
#         try:
#             return Favourite.objects.filter(user=request.user.id)
#         except Favourite.DoesNotExist:
#             raise Http404
#
#     def list(self, request):
#         favourite_company = self.get_queryset(self.request)
#         data = []
#         for el in favourite_company.values('company'):
#             company = Company.objects.get(id=el.get('company'))
#             data.append({
#                 'id': el.get('company'),
#                 'name': company.Company,
#                 'direction': company.Direction,
#                 'inn': company.INN,
#                 'address': company.Address,
#                 'url': company.URL,
#                 'telephone': company.Telephone
#             })
#         serializer = NewNewFavouriteSerializer(data, many=True)
#         return Response(serializer.data)


class FavouriteDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer

    def get(self,request):
        user = User.objects.get(id=request.user.id)
        favourite_company = Favourite.objects.filter(user=user)
        data = []
        for el in favourite_company.values('company'):
            company = Company.objects.get(id=el.get('company'))
            data.append({
                'id': el.get('company'),
                'name': company.Company,
                'direction': company.Direction,
                'inn': company.INN,
                'address': company.Address,
                'url': company.URL,
                'telephone': company.Telephone
                })
        serializer = NewNewFavouriteSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, **kwargs):
        """
        Добавляет компанию в избранное пользователя
        """
        try:
            data = request.data['favourite']
        except KeyError:
            return JsonResponse({'error': 'неверно указан ключ. Необходим ключ favourite'})

        user = User.objects.get(id=request.user.id)
        for _id in data:
            try:
                company = Company.objects.get(id=_id)
            except Company.DoesNotExist:
                JsonResponse({'error': 'неверный id'})

            if not Favourite.objects.filter(user=user, company=company).exists():
                Favourite.objects.create(user=User.objects.get(id=request.user.id), company=company)
        return JsonResponse({'detail': 'ok'})

    def delete(self, request, **kwargs):
        """
        Удаляет компанию из избранных юзера
        """
        try:
            data = request.data['favourite']
        except KeyError:
            return JsonResponse({'error': 'неверно указан ключ. Необходим ключ favourite'})

        user = User.objects.get(id=request.user.id)
        for _id in data:
            try:
                company = Company.objects.get(id=_id)
                favourite_company = Favourite.objects.get(user=user, company=company)
                favourite_company.delete()
                # return JsonResponse({'detail': 'Компания удалена из избранных'})
            except Favourite.DoesNotExist:
                return JsonResponse({'error': 'Компания не найдена'})
        return JsonResponse({'detail': 'ok'})


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
            find = last.last_request['find']
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
        except AttributeError:
            return Response({'error': 'Последних запросов нет'}, status=status.HTTP_400_BAD_REQUEST)


class QuantityApiList(APIView):
    """
    Возвращает количество компаний и продуктов в БД
    """
    # permission_classes = [IsAuthenticated]

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


class AnaliticsQuantityCompanyApiView(APIView):
    """
    Самые популярные категории - возвращает количество компаний в каждой категории
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sorted_dct = cache.get('analitics_categories', None)
            if not sorted_dct:
                dct = {}
                all_company = Company.objects.all()
                for company in all_company:
                    if company.Categories:
                        for el in company.Categories:
                            dct[el] = dct.get(el, 0) + 1
                sorted_tuples = sorted(dct.items(), key=lambda item: item[1], reverse=True)[:20]
                sorted_dct = {key: value for key, value in sorted_tuples}
                cache.set('analitics_categories', sorted_dct)
            return JsonResponse(sorted_dct)
        except Company.DoesNotExist:
            raise Http404


class AnaliticsQuantityDirectionApiView(APIView):
    """
    Самые популярные направления(direction) - возвращает количество компаний по каждому направлению
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sorted_dct = cache.get('analitics_directions', None)
            if not sorted_dct:
                dct = {}
                all_direction = Company.objects.all()
                for direction in all_direction:
                    dct[direction.Direction] = dct.get(direction.Direction, 0) + 1
                sorted_tuple = sorted(dct.items(), key=lambda item: item[1], reverse=True)[:20]
                sorted_dct = {key: value for key, value in sorted_tuple}
                cache.set('analitics_directions', sorted_dct)
            return JsonResponse(sorted_dct)
        except Company.DoesNotExist:
            raise Http404


class AnaliticsQuantityLocalityApiView(APIView):
    """
    Количество производителей по городам
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sorted_dct = cache.get('analitics_locality', None)
            if not sorted_dct:
                dct = {}
                all_locality = Company.objects.all()
                for locality in all_locality:
                    dct[locality.Locality] = dct.get(locality.Locality, 0) + 1
                sorted_tuple = sorted(dct.items(), key=lambda item: item[1], reverse=True)[:20]
                sorted_dct = {key: value for key, value in sorted_tuple}
                cache.set('analitics_locality', sorted_dct)
            return JsonResponse(sorted_dct)
        except Company.DoesNotExist:
            raise Http404

