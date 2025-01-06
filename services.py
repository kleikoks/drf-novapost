from .models import SettlementType, WarehouseType, Area, Settlement, Warehouse
from .utils import get_response, get_full_response


def test_api():
    response = get_response(model="Address", method="getSettlementTypes")
    if response["errors"]:
        raise Exception(response["errors"])


def create_settlement_types():
    response = get_response(model="Address", method="getSettlementTypes")
    bulk_create = []
    bulk_update = []
    settlement_types = SettlementType.objects.all()
    settlement_types_mapping = {s.ref: s for s in settlement_types}

    for obj in response["data"]:
        title = obj.get("Description")
        short_desc = obj.get("Code")
        ref = obj.get("Ref")

        settlement_type = settlement_types_mapping.get(ref)
        if settlement_type:
            settlement_type.title = title
            settlement_type.short_desc = short_desc
            bulk_update.append(settlement_type)
        else:
            bulk_create.append(
                SettlementType(title=title, short_desc=short_desc, ref=ref)
            )

    SettlementType.objects.bulk_create(bulk_create)
    SettlementType.objects.bulk_update(
        bulk_update, fields=("title", "short_desc")
    )
    print("SettlementType created -", len(bulk_create))
    print("SettlementType updated -", len(bulk_update))


def create_warehouse_types():
    response = get_response(model="Address", method="getWarehouseTypes")
    bulk_create = []
    bulk_update = []
    warehouse_types = WarehouseType.objects.all()
    warehouse_types_mapping = {w.ref: w for w in warehouse_types}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")

        warehouse_type = warehouse_types_mapping.get(ref)
        if warehouse_type:
            warehouse_type.title = title
            bulk_update.append(warehouse_type)
        else:
            bulk_create.append(WarehouseType(title=title, ref=ref))

    WarehouseType.objects.bulk_create(bulk_create)
    WarehouseType.objects.bulk_update(bulk_update, fields=("title",))
    print("WarehouseType created -", len(bulk_create))
    print("WarehouseType updated -", len(bulk_update))


def create_areas():
    response = get_response(model="Address", method="getAreas")
    bulk_create = []
    bulk_update = []
    areas = Area.objects.all()
    areas_mapping = {a.ref: a for a in areas}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")

        area = areas_mapping.get(ref)
        if area:
            area.title = title
            bulk_update.append(area)
        else:
            bulk_create.append(Area(title=title, ref=ref))

    Area.objects.bulk_create(bulk_create)
    Area.objects.bulk_update(bulk_update, fields=("title",))
    print("Area created -", len(bulk_create))
    print("Area updated -", len(bulk_update))


def create_settlements():
    response = get_full_response("Address", "getCities")
    bulk_create = []
    bulk_update = []
    areas = Area.objects.all()
    areas_mapping = {a.ref: a for a in areas}
    settlements = Settlement.objects.all()
    settlements_mapping = {s.ref: s for s in settlements}
    settlement_types = SettlementType.objects.all()
    settlement_types_mapping = {s.ref: s for s in settlement_types}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")
        settlement_type = settlement_types_mapping.get(obj.get("SettlementType"))
        area = areas_mapping.get(obj.get("Area"))

        settlement = settlements_mapping.get(ref)
        if settlement:
            settlement.title = title
            bulk_update.append(settlement)
        else:
            bulk_create.append(
                Settlement(title=title, type=settlement_type, ref=ref, area=area)
            )

    Settlement.objects.bulk_create(bulk_create)
    Settlement.objects.bulk_update(bulk_update, fields=("title",))
    print("Settlement created -", len(bulk_create))
    print("Settlement updated -", len(bulk_update))


def create_warehouses():
    response = get_full_response("Address", "getWarehouses")
    bulk_create = []
    bulk_update = []
    skipped = 0
    settlements = Settlement.objects.all()
    settlements_mapping = {s.ref: s for s in settlements}
    warehouses = Warehouse.objects.all()
    warehouse_mapping = {w.ref: w for w in warehouses}
    warehouse_types = WarehouseType.objects.all()
    warehouse_types_mapping = {w.ref: w for w in warehouse_types}

    for obj in response["data"]:
        title = obj.get("Description")
        ref = obj.get("Ref")
        short_address = obj["ShortAddress"]
        warehouse_type = warehouse_types_mapping.get(obj["TypeOfWarehouse"])
        settlement = settlements_mapping.get(obj["CityRef"])

        if not all((warehouse_type, settlement)):
            skipped += 1
            continue

        warehouse = warehouse_mapping.get(ref)
        if warehouse:
            warehouse.title = title
            warehouse.short_address = short_address
            warehouse.type = warehouse_type
            warehouse.settlement = settlement
            bulk_update.append(warehouse)
        else:
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
    Warehouse.objects.bulk_update(bulk_update, fields=("title", "short_address", "type", "settlement"))
    print("Warehouse created -", len(bulk_create))
    print("Warehouse updated -", len(bulk_update))
    print("Warehouse skipped -", skipped)
