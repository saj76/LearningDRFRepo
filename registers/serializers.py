from rest_framework import serializers
from registers.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.count()

    class Meta:
        model = Shop
        fields = ['status', 'name', 'owner', 'email', 'created_at', 'count']


class CustomShopSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass