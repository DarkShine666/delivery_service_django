import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from parcels.models import ParcelType, Parcel
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_endpoint(api_client):
    pt = ParcelType.objects.create(name="Books")
    url = reverse("parcel-register")
    response = api_client.post(
        url,
        {
            "type": pt.id,
            "weight_kg": 3.0,
            "declared_value_usd": "20.00",
            "destination_country": "FR",
        },
        format="json",
    )
    assert response.status_code == 201
    assert "id" in response.data


@pytest.mark.django_db
def test_list_and_filter(api_client):
    pt1 = ParcelType.objects.create(name="A")
    pt2 = ParcelType.objects.create(name="B")
    Parcel.objects.create(
        type=pt1,
        weight_kg=1,
        declared_value_usd=Decimal("10.00"),
        destination_country="X",
        session_key="s1",
    )
    Parcel.objects.create(
        type=pt2,
        weight_kg=2,
        declared_value_usd=Decimal("20.00"),
        destination_country="Y",
        session_key="s1",
    )
    url = reverse("parcel-list")
    resp = api_client.get(url, {"type": pt1.id})
    assert resp.status_code == 200
    assert len(resp.data["results"]) == 1


@pytest.mark.django_db
def test_detail_endpoint(api_client):
    pt = ParcelType.objects.create(name="Z")
    p = Parcel.objects.create(
        type=pt,
        weight_kg=1,
        declared_value_usd=Decimal("5.00"),
        destination_country="Z",
        session_key="s2",
    )
    url = reverse("parcel-detail", args=[p.id])
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data["destination_country"] == "Z"
