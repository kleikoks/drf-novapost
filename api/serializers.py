from rest_framework.serializers import ModelSerializer
from ..models import Settlement, Warehouse


class SettlementSerializer(ModelSerializer):
    class Meta:
        model = Settlement
        fields = ["id", "title"]


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "title", "short_address"]
