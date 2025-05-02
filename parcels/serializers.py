from rest_framework import serializers
from .models import Parcel, ParcelType


class ParcelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = ["type", "weight_kg", "declared_value_usd", "destination_country"]

    def create(self, validated_data):
        return Parcel.objects.create(**validated_data)


class ParcelSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name")

    class Meta:
        model = Parcel
        fields = [
            "id",
            "type",
            "weight_kg",
            "declared_value_usd",
            "destination_country",
            "registered_at",
            "delivery_price",
        ]


class ParcelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelType
        fields = ["id", "name"]
