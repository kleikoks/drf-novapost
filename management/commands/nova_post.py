from django.core.management.base import BaseCommand

from ...services import (
    test_api,
    create_settlement_types,
    create_warehouse_types,
    create_areas,
    create_settlements,
    create_warehouses
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        test_api()
        create_settlement_types()
        create_warehouse_types()
        create_areas()
        create_settlements()
        create_warehouses()
