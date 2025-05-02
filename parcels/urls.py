from django.urls import path, include
from .views import (
    RegisterParcelView,
    ParcelListView,
    ParcelDetailView,
    ParcelTypeListCreateView,
    ParcelTypeDetailView,
)


urlpatterns = [
    path("register/", RegisterParcelView.as_view(), name="parcel-register"),
    path("list/", ParcelListView.as_view(), name="parcel-list"),
    path("<int:pk>/", ParcelDetailView.as_view(), name="parcel-detail"),
    path("types/", ParcelTypeListCreateView.as_view(), name="parceltype-list-create"),
    path("types/<int:pk>/", ParcelTypeDetailView.as_view(), name="parceltype-detail"),
]
