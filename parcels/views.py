from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from parcels.tasks import calculate_delivery_price
from parcels.models import Parcel, ParcelType
from parcels.serializers import (
    ParcelRegisterSerializer,
    ParcelSerializer,
    ParcelTypeSerializer,
)
import logging

logger = logging.getLogger("parcels")


class ParcelPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RegisterParcelView(generics.GenericAPIView, CreateModelMixin):
    queryset = Parcel.objects.all()
    serializer_class = ParcelRegisterSerializer

    def post(self, request, *args, **kwargs):
        logger.info("Запрос на регистрацию посылки", extra={"data": request.data})
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            logger.warning(
                "Ошибка валидации при регистрации посылки", extra={"errors": e.detail}
            )
            raise

        parcel = serializer.save(session_key=session_key)
        logger.debug(f"Создана посылка {parcel.id} для сессии {session_key}")
        calculate_delivery_price.delay(parcel.id)
        return Response({"id": parcel.id}, status=status.HTTP_201_CREATED)


class ParcelListView(generics.ListAPIView):
    serializer_class = ParcelSerializer
    pagination_class = ParcelPagination

    def get_queryset(self):
        params = self.request.query_params.dict()
        logger.info("Запрос списка посылок", extra={"filters": params})

        queryset = Parcel.objects.all()
        type_id = self.request.query_params.get("type")
        destination = self.request.query_params.get("destination_country")
        min_weight = self.request.query_params.get("weight_kg__gte")
        max_weight = self.request.query_params.get("weight_kg__lte")

        if type_id:
            queryset = queryset.filter(type_id=type_id)
        if destination:
            queryset = queryset.filter(destination_country__icontains=destination)
        if min_weight:
            queryset = queryset.filter(weight_kg__gte=min_weight)
        if max_weight:
            queryset = queryset.filter(weight_kg__lte=max_weight)

        return queryset


class ParcelDetailView(generics.RetrieveAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

    def get(self, request, *args, **kwargs):
        parcel_id = kwargs.get("pk")
        logger.info(f"Запрос деталей посылки id={parcel_id}")
        return super().get(request, *args, **kwargs)


class ParcelTypeListView(generics.ListAPIView):
    queryset = ParcelType.objects.all()
    serializer_class = ParcelTypeSerializer
