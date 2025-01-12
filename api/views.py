from django.db.models import Q, Case, When, IntegerField, Value, QuerySet
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from ..models import Warehouse, Settlement
from .serializers import (
    WarehouseSerializer,
    SettlementSerializer,
)

from typing import TypeVar


A = TypeVar("A")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


def filter_title(queryset: QuerySet[A], query: str) -> QuerySet[A]:
    queryset = queryset.filter(
        Q(title__iexact=query) | Q(title__istartswith=query) | Q(title__icontains=query)
    ).annotate(
        priority=Case(
            When(title__iexact=query, then=0),
            When(title__istartswith=query, then=1),
            When(title__icontains=query, then=2),
            default=Value(999),
            output_field=IntegerField()
        )
    ).order_by('priority')
    return queryset


class SettlementsViewSet(GenericViewSet, ListModelMixin):
    serializer_class = SettlementSerializer
    queryset = Settlement.objects.all()
    pagination_class = StandardResultsSetPagination
    lookup_field = "ref"

    def get_queryset(self):
        query = self.request.query_params.get("q")

        if not query:
            return Settlement.objects.none()

        queryset = filter_title(queryset=self.queryset, query=query)
        return queryset

    @action(methods=["get"], detail=True)
    def warehouses(self, request, ref: str, *args, **kwargs):
        query = self.request.query_params.get("q")
        queryset = Warehouse.objects.filter(settlement__ref=ref)
        if query:
            queryset = filter_title(queryset=queryset, query=query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = WarehouseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WarehouseSerializer(queryset, many=True)
        return Response(serializer.data)
