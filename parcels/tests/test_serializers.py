import pytest
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from parcels.serializers import ParcelRegisterSerializer, ParcelSerializer
from parcels.models import ParcelType, Parcel


@pytest.mark.django_db
def test_register_serializer_valid():
    pt = ParcelType.objects.create(name="Misc")
    data = {
        "type": pt.id,
        "weight_kg": 1.2,
        "declared_value_usd": "50.00",
        "destination_country": "USA",
    }
    ser = ParcelRegisterSerializer(data=data)
    assert ser.is_valid(), ser.errors
    p = ser.save(session_key="sess1")
    assert isinstance(p, Parcel)
    assert p.session_key == "sess1"


@pytest.mark.django_db
def test_serializer_output_fields():
    pt = ParcelType.objects.create(name="Misc")
    p = Parcel.objects.create(
        type=pt,
        weight_kg=1.2,
        declared_value_usd=Decimal("50.00"),
        destination_country="USA",
        session_key="sess1",
    )
    ser = ParcelSerializer(p)
    out = ser.data
    assert out["id"] == p.id
    assert out["type"] == pt.name
    assert out["declared_value_usd"] == "50.00"
    assert out["delivery_price"] is None
