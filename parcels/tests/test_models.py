import pytest
from decimal import Decimal
from parcels.models import ParcelType, Parcel


@pytest.mark.django_db
def test_parcel_type_str():
    pt = ParcelType.objects.create(name="Electronics")
    assert str(pt) == "Electronics"


@pytest.mark.django_db
def test_parcel_creation_and_defaults():
    pt = ParcelType.objects.create(name="Clothes")
    p = Parcel.objects.create(
        type=pt,
        weight_kg=2.5,
        declared_value_usd=Decimal("100.00"),
        destination_country="Germany",
        session_key="abc123",
    )
    assert p.id is not None
    assert p.delivery_price is None
    assert p.registered_at is not None
