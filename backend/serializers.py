from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Company, Favourite


class RegionSerializer(serializers.Serializer):
    Region = serializers.CharField()


class LocalitySerializer(serializers.Serializer):
    Locality = serializers.CharField()


class CategoriesSerializer(serializers.Serializer):
    Categories = serializers.CharField()


class ProductsSerializer(serializers.Serializer):
    Products = serializers.CharField()


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('id',)


class NewFavouriteSerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields = ('id', 'Company',)


class NewNewFavouriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    direction = serializers.CharField()
    inn = serializers.CharField()
    address = serializers.CharField()
    url = serializers.CharField()
    telephone = serializers.CharField()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
