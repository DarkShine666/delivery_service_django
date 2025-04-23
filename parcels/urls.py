from django.urls import path
from .views import (
    RegisterParcelView,
    ParcelListView,
    ParcelDetailView,
    ParcelTypeListView,
)

urlpatterns = [
    path("register/", RegisterParcelView.as_view(), name="parcel-register"),
    path("list/", ParcelListView.as_view(), name="parcel-list"),
    path("<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
    path("types/", ParcelTypeListView.as_view(), name="parcel-types"),
]
