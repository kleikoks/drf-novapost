from django.conf import settings
from django.db import connection, OperationalError

from .models import SettlementType, WarehouseType, Area, Settlement, Warehouse
from .utils import get_response, get_full_response


def test_api():
    response = get_response(model="Address", method="getSettlementTypes")
    if response["errors"]:
        raise Exception(response["errors"])


def truncate_table(model):
    """rewrite it for your database"""
    with connection.cursor() as cursor:
        try:
            cursor.execute(f'TRUNCATE TABLE "{model._meta.db_table}";')  # postgres
        except OperationalError:
            try:
                cursor.execute(f'DELETE FROM "{model._meta.db_table}";')  # sqlite
            except OperationalError as e:
                print(e)


def cleanup():
    models = (Area, Settlement, SettlementType, Warehouse, WarehouseType)
    for model in models:
        truncate_table(model)


def create_settlement_types():
    response = get_response(model="Address", method="getSettlementTypes")
    bulk_create = []

    for obj in response["data"]:
        title = obj.get("Description")
        short_desc = obj.get("Code")
        ref = obj.get("Ref")
        bulk_create.append(
            SettlementType(title=title, short_desc=short_desc, ref=ref)
        )

    SettlementType.objects.bulk_create(bulk_create)
    print("SettlementType created -", len(bulk_create))


def create_warehouse_types():
    response = get_response(model="Address", method="getWarehouseTypes")
    bulk_create = []

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")

        bulk_create.append(WarehouseType(title=title, ref=ref))

    WarehouseType.objects.bulk_create(bulk_create)
    print("WarehouseType created -", len(bulk_create))


def create_areas():
    response = get_response(model="Address", method="getAreas")
    bulk_create = []

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")

        bulk_create.append(Area(title=title, ref=ref))

    Area.objects.bulk_create(bulk_create)
    print("Area created -", len(bulk_create))


def create_settlements():
    response = get_full_response("Address", "getCities")
    bulk_create = []
    areas = Area.objects.all()
    areas_mapping = {a.ref: a for a in areas}
    settlement_types = SettlementType.objects.all()
    settlement_types_mapping = {s.ref: s for s in settlement_types}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")
        settlement_type = settlement_types_mapping.get(obj.get("SettlementType"))
        area = areas_mapping.get(obj.get("Area"))

        bulk_create.append(
            Settlement(title=title, type=settlement_type, ref=ref, area=area)
        )

    Settlement.objects.bulk_create(bulk_create)
    print("Settlement created -", len(bulk_create))


def create_warehouses():
    response = get_full_response("Address", "getWarehouses")
    bulk_create = []
    settlements = Settlement.objects.all()
    settlements_mapping = {s.ref: s for s in settlements}
    warehouse_types = WarehouseType.objects.all()
    warehouse_types_mapping = {w.ref: w for w in warehouse_types}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")
        short_address = obj["ShortAddress"]
        warehouse_type = warehouse_types_mapping.get(obj["TypeOfWarehouse"])
        settlement = settlements_mapping.get(obj["CityRef"])

        bulk_create.append(
            Warehouse(
                title=title,
                short_address=short_address,
                type=warehouse_type,
                settlement=settlement,
                ref=ref,
            )
        )

    Warehouse.objects.bulk_create(bulk_create)
    print("Warehouse created -", len(bulk_create))
