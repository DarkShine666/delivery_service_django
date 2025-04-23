from django.db import models


class ParcelType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    type = models.ForeignKey(ParcelType, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    declared_value_usd = models.DecimalField(max_digits=10, decimal_places=2)
    destination_country = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, db_index=True)
    delivery_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Parcel {self.id} to {self.destination_country}"
