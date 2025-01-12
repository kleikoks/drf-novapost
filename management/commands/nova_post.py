from django.db import transaction
from django.core.management.base import BaseCommand

from ...services import (
    test_api,
    cleanup,
    create_settlement_types,
    create_warehouse_types,
    create_areas,
    create_settlements,
    create_warehouses
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        test_api()

        with transaction.atomic():
            cleanup()
            create_settlement_types()
            create_warehouse_types()
            create_areas()
            create_settlements()
            create_warehouses()
